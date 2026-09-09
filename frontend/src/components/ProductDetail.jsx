import React from 'react'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'

import { useDispatch } from 'react-redux'
import { addToCart } from '../store/CartSlice'
import '../style/Urundetay.css'
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from '../services/constants'

function UrunDetay() {
    const navigate = useNavigate()
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [alici, setAlici] = useState(null)
    const [satici, setSatici] = useState(null)

    const [reviews, setReviews] = useState([]);
    const [newReviewText, setNewReviewText] = useState("");
    const [rating, setRating] = useState(5);

    const [activeImage, setActiveImage] = useState(null);

    const [isChatOpen, setIsChatOpen] = useState(false);
    const [mesajlar, setMesajlar] = useState([]);
    const [yeniMesaj, setYeniMesaj] = useState("");
    const [mesajlasmaAlaniId, setMesajlasmaAlaniId] = useState(null);
    const [katilimcilar, setKatilimcilar] = useState([])

    const isSeller = localStorage.getItem('is_seller') === 'true';

    const [ws, setWs] = useState(null);

    const token = localStorage.getItem(ACCESS_TOKEN);
    let myUserId = null;

    if (token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            myUserId = String(payload.user_id);
        } catch (error) {
            console.error("Token çözümlenirken hata oluştu:", error);
        }
    }

    const dispatch = useDispatch();

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await api.get('accounts/listele/')
                setAlici(response.data)
            } catch (error) {
                console.error("KUllanıcı çekilirken bir hata oluştu:", error)
            }
        }
        fetchUser();
    }, [])

    useEffect(() => {
        if (product && product.seller) {
            const FetchSellerProfile = async () => {
                try {
                    const res = await api.get(`accounts/satici/${product.seller}/`);
                    setSatici(res.data);
                    console.log("Satıcının bilgileri:", res.data);
                } catch (error) {
                    console.error("Satıcı bilgileri çekilirken hata oluştu:", error);
                }
            }
            FetchSellerProfile();
        }
    }, [product])

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await api.get(`urunler/Urunliste/${id}/`)
                setProduct(response.data)
                setActiveImage(response.data.photo)
            } catch (error) {
                console.error("Ürün detayları çekilirken hata oluştu:", error)
            }
        }
        fetchProduct();
    }, [id])

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await api.get(`urunler/Urunliste/${id}/yorumlar/`)
                setReviews(response.data)
            } catch (error) {
                console.error("yorumlar çekilemedi", error)
            }
        }
        fetchReviews();
    }, [id])

    const handleAddReview = async (e) => {
        e.preventDefault();

        try {
            const response = await api.post(`urunler/Urunliste/${id}/yorumlar/`, {
                message: newReviewText,
                rating: parseInt(rating)
            });
            setReviews([response.data, ...reviews]);
            setNewReviewText("")
            alert("Yorumunuz başarı ile eklenmiştir")
        } catch (error) {
            console.error("yorum yapılamadı", error)
            alert("Sadece bu ürünü satın alan kullanıcılar yorum yapabilir.");
        }
    }

    const handleAddToCart = () => {
        dispatch(addToCart(product));
        alert(`${product.name} sepete eklendi!`);
    }

    useEffect(() => {
        if (product && isSeller === false) {
            const fetchConversationData = async () => {
                try {
                    const odaRes = await api.get(`chat/alan/kontrol/${product.seller}/`);

                    if (odaRes.data && odaRes.data.id) {
                        const varOlanOdaId = odaRes.data.id;

                        setMesajlasmaAlaniId(varOlanOdaId);

                        const mesajlarRes = await api.get(`chat/mesaj/listele/${varOlanOdaId}/`);

                        const formatliMesajlar = mesajlarRes.data.map(msg => {
                            console.log("Geçmiş Mesaj Testi -> Gelen:", msg.gönderici, "| Benim ID:", myUserId);

                            return {
                                gönderici: { id: msg.gönderici },
                                icerik: msg.icerik,
                                gönderilme_tarihi: msg.gönderilme_tarihi,
                                bizimMi: String(msg.gönderici) === String(myUserId)
                            };
                        });

                        setMesajlar(formatliMesajlar);
                    }
                } catch (error) {
                    if (error.response && error.response.status === 404) {
                        console.log("Bu satıcıyla henüz sohbet başlatılmamış. İlk mesajı bekliyor.");
                    } else {
                        console.error("Geçmiş sohbet kontrolü sırasında hata:", error);
                    }
                }
            }
            fetchConversationData();
        }
    }, [product, isSeller, myUserId])

    useEffect(() => {
        if (!mesajlasmaAlaniId) return;

        let websocket = null;
        let reconnectTimeout = null;
        let isUnmounting = false;

        const connect = () => {
            if (isUnmounting) return;

            const token = localStorage.getItem(ACCESS_TOKEN);
            websocket = new WebSocket(
                `ws://127.0.0.1:8000/ws/chat/${mesajlasmaAlaniId}/?token=${token}`
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
    }, [mesajlasmaAlaniId])

    const alanolustur = async (e) => {
        e.preventDefault();

        if (yeniMesaj.trim() === "") return;

        try {
            const alanresponse = await api.post(
                "chat/alan/olustur/",
                {
                    satici_id: satici.id
                });

            const yeniAlanId = alanresponse.data.id;

            await api.post("chat/mesaj/olustur/", {
                mesajlasma_alani: yeniAlanId,
                icerik: yeniMesaj
            })

            setMesajlar([{ icerik: yeniMesaj, bizimMi: true }]);
            setYeniMesaj("");

            setMesajlasmaAlaniId(yeniAlanId);
        } catch (error) {
            console.error("Oda oluşturulurken hata:", error);
            alert("Mesaj başlatılamadı.");
        }
    }


    const mesajGönder = async (e) => {
        if (!mesajlasmaAlaniId || !yeniMesaj.trim()) return;

        if (ws?.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                mesaj: yeniMesaj
            }));
            setYeniMesaj("");
        } else {
            console.error("Websocket açık değil")
        }
    }

    return (
        <div className="product-detail">
            {product && (
                <div className="product-detail__layout">
                    <div style={{ width: '100%' }}>
                        <div style={{ width: '100%', height: '400px', border: '1px solid #ccc', borderRadius: '8px', overflow: 'hidden', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <img
                                src={activeImage}
                                alt={product.name}
                                style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                            />
                        </div>
                        <div style={{ display: 'flex', gap: '10px', marginTop: '15px', overflowX: 'auto' }}>

                            <img
                                src={product.photo}
                                alt="Kapak"
                                onClick={() => setActiveImage(product.photo)}
                                style={{
                                    width: '80px', height: '80px', cursor: 'pointer', objectFit: 'cover', borderRadius: '5px',
                                    border: activeImage === product.photo ? '3px solid #007bff' : '1px solid #ddd'
                                }}
                            />


                            {product.images && product.images.map((item) => (
                                <img
                                    key={item.id}
                                    src={item.image}
                                    alt="Ekstra"
                                    onClick={() => setActiveImage(item.image)}
                                    style={{
                                        width: '80px', height: '80px', cursor: 'pointer', objectFit: 'cover', borderRadius: '5px',
                                        border: activeImage === item.image ? '3px solid #007bff' : '1px solid #ddd'
                                    }}
                                />
                            ))}
                        </div>

                    </div>

                    <div className="product-detail__info">
                        <span className="product-detail__seller">Satıcı: {product.seller}</span>
                        <h2 className="product-detail__name">{product.name}</h2>
                        <p className="product-detail__description">{product.description}</p>

                        <div className="product-detail__price-tag">
                            <span className="product-detail__price">{product.price} ₺</span>
                        </div>

                        <ul className="product-detail__facts">
                            <li>
                                <span>Stok</span>
                                <strong>{product.stock_count}</strong>
                            </li>
                            <li>
                                <span>Adet</span>
                                <strong>{product.quantity}</strong>
                            </li>
                        </ul>

                        <button className="product-detail__cta" onClick={handleAddToCart}>
                            Sepete Ekle
                        </button>
                        <h1>Satıcı:</h1>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }} onClick={() => navigate(`/satici/${product.seller}`)}>
                            <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: '#ccc', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                👤
                            </div>
                            <div style={{ display: 'flex', flexDirection: 'column' }}>
                                <span style={{ fontSize: '14px', fontWeight: 'bold' }}>{product.seller_name}</span>
                                <span style={{ fontSize: '12px', color: 'gray' }}>Hesap Yok</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
            <div>
                <h3>Ürün yorumları ({reviews.length})</h3>
                <form onSubmit={handleAddReview}>
                    <div>
                        <input
                            type='text'
                            value={newReviewText}
                            onChange={(e) => setNewReviewText(e.target.value)}
                            required
                        />
                        <select
                            value={rating}
                            onChange={(e) => setRating(e.target.value)}
                            required
                        >
                            <option value={5}>5 Yıldız</option>
                            <option value={4}>4 Yıldız</option>
                            <option value={3}>3 Yıldız</option>
                            <option value={2}>2 Yıldız</option>
                            <option value={1}>1 Yıldız</option>
                        </select>
                        <button type='submit'>Gönder</button>
                    </div>
                </form>

                <div>
                    {reviews.length === 0 ? (
                        <p>Bu ürüne henüz yorum yapılmamış</p>
                    ) : (
                        <ul>
                            {reviews.map((review) => (
                                <li key={review.id}>
                                    <div>
                                        <strong>{review.username}</strong>
                                        <span>{review.username}</span>
                                        {review.is_buyed && (
                                            <span>
                                                ✅ Ürünü Satın Aldı
                                            </span>
                                        )}
                                    </div>
                                    <p>{review.message}</p>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
            {!isSeller && (
                <div style={{ position: 'fixed', bottom: '30px', right: '30px', zIndex: 1000 }}>
                    {!isChatOpen ? (
                        <button
                            onClick={() => setIsChatOpen(true)}
                            style={{ padding: '15px 25px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '30px', cursor: 'pointer', boxShadow: '0 4px 12px rgba(0,0,0,0.15)', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '16px', fontWeight: 'bold' }}
                        >
                            <span>💬</span> Satıcıya Soru Sor
                        </button>
                    ) : (
                        <div style={{ width: '350px', height: '480px', backgroundColor: '#fff', borderRadius: '12px', boxShadow: '0 8px 24px rgba(0,0,0,0.2)', display: 'flex', flexDirection: 'column', overflow: 'hidden', border: '1px solid #e0e0e0' }}>


                            <div style={{ backgroundColor: '#007bff', padding: '15px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'white' }}>
                                <div style={{ display: 'flex', flexDirection: 'column' }}>
                                    <span style={{ fontWeight: 'bold', fontSize: '15px' }}>{product.seller_name}</span>
                                    <span style={{ fontSize: '12px', opacity: 0.8 }}>Satıcı ile sohbet ediyorsunuz</span>
                                </div>
                                <button
                                    onClick={() => setIsChatOpen(false)}
                                    style={{ background: 'none', border: 'none', color: 'white', fontSize: '24px', cursor: 'pointer', lineHeight: '1' }}
                                >
                                    ×
                                </button>
                            </div>


                            <div style={{ flex: 1, padding: '15px', backgroundColor: '#f8f9fa', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                                {mesajlar.length === 0 ? (
                                    <div style={{ textAlign: 'center', color: '#6c757d', fontSize: '14px', marginTop: '20px' }}>
                                        <span style={{ fontSize: '30px', display: 'block', marginBottom: '10px' }}>👋</span>
                                        Satıcıya ürünle ilgili sorularınızı sorabilirsiniz.
                                    </div>
                                ) : (
                                    mesajlar.map((msg, index) => (
                                        <div
                                            key={index}
                                            style={{
                                                maxWidth: '80%',
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


                            <form
                                onSubmit={(e) => {
                                    e.preventDefault();
                                    if (mesajlar.length === 0 && isSeller === false) {
                                        alanolustur(e);
                                    } else if (mesajlar.length === 0 && isSeller === true) {
                                        alert("satıcılar mesaj müşteri mesajlaşma başlatmadan mesaj gönderemez")
                                    } else if (mesajlar.length > 0) {
                                        if (yeniMesaj.trim() === "") {
                                            alert("Mesaj boş bırakılamaz");
                                        } else {
                                            mesajGönder();
                                        }
                                    }
                                }}
                                style={{ padding: '15px', backgroundColor: 'white', borderTop: '1px solid #eee', display: 'flex', gap: '10px' }}
                            >
                                <input
                                    type="text"
                                    value={yeniMesaj}
                                    onChange={(e) => setYeniMesaj(e.target.value)}
                                    placeholder="Mesajınızı yazın..."
                                    style={{ flex: 1, padding: '10px 15px', border: '1px solid #ddd', borderRadius: '20px', outline: 'none', fontSize: '14px' }}
                                />
                                <button
                                    type="submit"
                                    style={{ backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '50%', width: '40px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}
                                >
                                    <span>➤</span>
                                </button>
                            </form>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default UrunDetay