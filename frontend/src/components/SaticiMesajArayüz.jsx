import React, { useEffect, useState } from 'react'
import api from '../services/api'
import { useNavigate } from 'react-router-dom';



function SaticiMesajArayüz() {
    const navigate = useNavigate()
    const [odalar, setOdalar] = useState([]);

    useEffect(() => {
        const fetchConversationsData = async () => {
            try {
                const response = await api.get('chat/alan/kontrol/satici/')
                setOdalar(response.data)
            } catch (error) {
                console.error("Sohbet odaları çekilirken hata:", error);
            }
        }
        fetchConversationsData();
    }, [])
    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <h2>Gelen Mesajlar (Sohbet Odaları)</h2>
            {odalar.length === 0 ? (
                <p>Henüz kimse size mesaj göndermemiş.</p>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {odalar.map((oda) => (
                        <div
                            key={oda.id}
                            style={{
                                padding: '15px',
                                border: '1px solid #ddd',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                backgroundColor: '#f9f9f9'
                            }}
                            onClick={() => navigate(`/saticiMesajAlani/${oda.id}`)}
                        >
                            <h3>Müşteri ID: {oda.alici}</h3>
                            <p style={{ color: 'gray', fontSize: '12px' }}>
                                Oda No: {oda.id}
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )

}

export default SaticiMesajArayüz