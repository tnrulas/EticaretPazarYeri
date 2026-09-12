import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { ACCESS_TOKEN } from '../services/constants';
import { useState, useEffect } from 'react';

function SaticiMesajAlani() {
    const { odaId } = useParams();
    const navigate = useNavigate();

    const [mesajlar, setMesajlar] = useState([]);
    const [yeniMesaj, setYeniMesaj] = useState("");
    const [ws, setWs] = useState(null);

    const token = localStorage.getItem(ACCESS_TOKEN);
    let myUserId = null;

    if (token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            myUserId = String(payload.user_id)
        } catch (error) {
            console.error("Token çözümlenirken hata oluştu:", error);
        }
    }

    useEffect(() => {
        const fetchConversationData = async () => {
            try {
                const mesajlarRes = await api.get(`chat/mesaj/listele/${odaId}/`);
                const formatliMesajlar = mesajlarRes.data.map(msg => {
                    return {
                        gönderici: { id: msg.gönderici },
                        icerik: msg.icerik,
                        gönderilme_tarihi: msg.gönderilme_tarihi,
                        bizimMi: String(msg.gönderici) === String(myUserId)
                    };
                });
                setMesajlar(formatliMesajlar);
            } catch (error) {
                if (error.response && error.response.status === 404) {
                    console.log("Bu satıcıyla henüz sohbet başlatılmamış.");
                } else {
                    console.error("Geçmiş sohbet çekilirken hata:", error);
                }
            }
        };
        if (odaId) fetchConversationData();
    }, [odaId, myUserId]);

    useEffect(() => {
        if (!odaId) return;

        let websocket = null;
        let reconnectTimeout = null;
        let isUnmounting = false;

        const connect = () => {
            if (isUnmounting) return;

            const token = localStorage.getItem(ACCESS_TOKEN);
            websocket = new WebSocket(
                `ws://127.0.0.1:8000/ws/chat/${odaId}/?token=${token}`
            );

            websocket.onopen = () => {
                console.log("WebSocket açıldı");
                setWs(websocket)
            }

            websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);

                if (data.type === "chat_message") {
                    const gonderenId = data.id;
                    const gelenIcerik = data.mesaj;

                    setMesajlar((prev) => [
                        ...prev,
                        {
                            icerik: gelenIcerik,
                            gönderilme_tarihi: data.gönderilme_tarihi,
                            bizimMi: String(gonderenId) === String(myUserId)
                        }
                    ]);
                }
            };

            websocket.onclose = async () => {
                setWs(null);
                if (!isUnmounting) {
                    console.log("Yeniden bağlanılıyor...");
                    reconnectTimeout = setTimeout(connect, 2000);
                }
            };

            websocket.onerror = () => {
                websocket.close();
            };
        }
        connect();

        return () => {
            isUnmounting = true;
            if (reconnectTimeout) clearTimeout(reconnectTimeout);
            if (websocket) websocket.close();
        };
    }, [odaId, myUserId])

    const mesajGonder = async (e) => {
        e.preventDefault();
        if (!odaId || !yeniMesaj.trim()) return;

        if (ws?.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                mesaj: yeniMesaj
            }));
            setYeniMesaj("");
        } else {
            console.error("Websocket açık değil")
        }
    }

    useEffect(() => {
        console.log("aaaaaaaaa", mesajlar)
    }, [mesajlar])
    return (
        <div style={{ maxWidth: '800px', margin: '20px auto', border: '1px solid #ccc', borderRadius: '10px', height: '600px', display: 'flex', flexDirection: 'column', backgroundColor: '#fff', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>

            <div style={{ padding: '15px', backgroundColor: '#007bff', color: 'white', borderTopLeftRadius: '10px', borderTopRightRadius: '10px', display: 'flex', alignItems: 'center', gap: '15px' }}>
                <button
                    onClick={() => navigate(`/saticiMesajlar/${myUserId}`)}
                    style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer', fontSize: '18px' }}
                >
                    ← Geri
                </button>
                <div style={{ display: 'flex', flexDirection: 'column' }}>
                    <h3 style={{ margin: 0, fontSize: '16px' }}>Müşteri ile Sohbet</h3>
                    <span style={{ fontSize: '12px', opacity: 0.8 }}>Oda #{odaId}</span>
                </div>
            </div>

            <div style={{ flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '10px', backgroundColor: '#f8f9fa' }}>
                {mesajlar.length === 0 ? (
                    <div style={{ textAlign: 'center', color: '#6c757d', marginTop: '20px' }}>
                        Geçmiş mesaj bulunmuyor.
                    </div>
                ) : (
                    mesajlar.map((msg, index) => (
                        <div
                            key={index}
                            style={{
                                maxWidth: '70%',
                                padding: '10px 14px',
                                borderRadius: '15px',
                                alignSelf: msg.bizimMi ? 'flex-end' : 'flex-start',
                                backgroundColor: msg.bizimMi ? '#007bff' : '#e9ecef',
                                color: msg.bizimMi ? 'white' : '#212529',
                                fontSize: '14px',
                                borderBottomRightRadius: msg.bizimMi ? '4px' : '15px',
                                borderBottomLeftRadius: msg.bizimMi ? '15px' : '4px'
                            }}
                        >
                            {msg.icerik}
                        </div>
                    ))
                )}
            </div>

            <form onSubmit={mesajGonder} style={{ padding: '15px', backgroundColor: 'white', borderTop: '1px solid #eee', display: 'flex', gap: '10px', borderBottomLeftRadius: '10px', borderBottomRightRadius: '10px' }}>
                <input
                    type="text"
                    value={yeniMesaj || ""}
                    onChange={(e) => setYeniMesaj(e.target.value)}
                    placeholder="Mesajınızı yazın..."
                    style={{ flex: 1, padding: '10px 15px', border: '1px solid #ddd', borderRadius: '20px', outline: 'none', fontSize: '14px' }}
                />
                <button
                    type="submit"
                    style={{ backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '50%', width: '42px', height: '42px', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}
                >
                    <span style={{ transform: 'translateX(-2px)' }}>➤</span>
                </button>
            </form>

        </div>
    )
}

export default SaticiMesajAlani;