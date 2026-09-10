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

    const [favoriler, setFavoriler] = useState([]);
    const isFavorited = product ? favoriler.includes(product.id) : false;

    const isSeller = localStorage.getItem('is_seller') === 'true';

    const [ws, setWs] = useState(null);

    const token = localStorage.getItem(ACCESS_TOKEN);
    let myUserId = null;

    const [onerilenUrunler, setOnerilenUrunler] = useState([]);

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
        if (product && product.id) {
            const fetchOneriler = async () => {
                try {
                    const response = await api.get(`urunler/urunler/${product.id}/oneriler/`);
                    setOnerilenUrunler(response.data);
                    console.log("Çekilen Öneriler:", response.data);
                } catch (error) {
                    console.error("Önerilen ürünler çekilemedi:", error);
                }
            }
            fetchOneriler();
        }
    }, [product]);

    useEffect(() => {
        const fetchFavorites = async () => {
            try {
                const response = await api.get('accounts/favorilerim/');
                const favoriteIds = response.data.map(item => item.id);
                setFavoriler(favoriteIds);
            } catch (error) {
                console.error("Favoriler çekilirken hata oluştu:", error);
            }
        }
        fetchFavorites();
    }, [])

    const addFavorites = async (id) => {
        try {
            const response = await api.post(`accounts/favori-islem/${id}/`)

            if (response.data.durum) {
                setFavoriler([...favoriler, id])
            } else {
                setFavoriler(favoriler.filter(favId => favId !== id))
            }
        } catch (error) {
            console.error("Favori işlemi başarısız:", error);
        }
    }

    // ---------------------------------------------------------------------------------
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
        <div className="product-detail-container">
            {product && (
                <div className="product-split-layout">
                    <div className="gallery-section">
                        <div className="main-image-card">
                            <img
                                src={activeImage}
                                alt={product.name}
                            />
                        </div>
                        <div className="thumbnail-strip">
                            <div
                                className={`thumbnail-item ${activeImage === product.photo ? 'active' : ''}`}
                                onClick={() => setActiveImage(product.photo)}
                            >
                                <img src={product.photo} alt="Kapak" />
                            </div>

                            {product.images && product.images.map((item) => (
                                <div
                                    className={`thumbnail-item ${activeImage === item.image ? 'active' : ''}`}
                                    key={item.id}
                                    onClick={() => setActiveImage(item.image)}
                                >
                                    <img src={item.image} alt="Ekstra" />
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="info-section">
                        <div className="seller-tag" onClick={() => navigate(`/satici/${product.seller}`)}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                            Satıcı: {product.seller_name}
                        </div>

                        <h1 className="product-title">{product.name}</h1>
                        <p className="product-desc">{product.description}</p>

                        <div className="price-box">
                            <span className="price-amount">{product.price} ₺</span>
                        </div>

                        <div className="inventory-stats">
                            <div className="stat-item">
                                <span className="stat-label">Stok Durumu</span>
                                <span className="stat-value">{product.stock_count} Adet</span>
                            </div>
                            <div className="stat-item">
                                <span className="stat-label">Toplam Satış</span>
                                <span className="stat-value">{product.quantity}</span>
                            </div>
                        </div>

                        <div className="action-group">
                            <button className="btn-add-cart" onClick={handleAddToCart}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                                Sepete Ekle
                            </button>

                            <button
                                className={`btn-favorite-large ${isFavorited ? 'is-active' : ''}`}
                                onClick={(e) => {
                                    e.stopPropagation();
                                    addFavorites(product.id);
                                }}
                                title={isFavorited ? "Favorilerden Çıkar" : "Favorilere Ekle"}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill={isFavorited ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
                            </button>
                        </div>
                    </div>
                </div>
            )}
            <div className="reviews-section">
                <h3 className="reviews-header">Değerlendirmeler ({reviews.length})</h3>

                <div className="review-form-card">
                    <form className="review-form-inner" onSubmit={handleAddReview}>
                        <input
                            className="review-input"
                            type='text'
                            value={newReviewText}
                            placeholder="Ürün hakkındaki düşüncelerinizi paylaşın..."
                            onChange={(e) => setNewReviewText(e.target.value)}
                            required
                        />
                        <select
                            className="review-select"
                            value={rating}
                            onChange={(e) => setRating(e.target.value)}
                            required
                        >
                            <option value={5}>⭐⭐⭐⭐⭐ (5 Yıldız)</option>
                            <option value={4}>⭐⭐⭐⭐ (4 Yıldız)</option>
                            <option value={3}>⭐⭐⭐ (3 Yıldız)</option>
                            <option value={2}>⭐⭐ (2 Yıldız)</option>
                            <option value={1}>⭐ (1 Yıldız)</option>
                        </select>
                        <button className="btn-submit-review" type='submit'>Gönder</button>
                    </form>
                </div>

                <div className="reviews-list">
                    {reviews.length === 0 ? (
                        <p style={{ color: 'var(--color-ink-faint)', textAlign: 'center', padding: '2rem' }}>Henüz değerlendirme yapılmamış. İlk değerlendiren siz olun!</p>
                    ) : (
                        reviews.map((review) => (
                            <div className="review-card" key={review.id}>
                                <div className="review-meta">
                                    <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'var(--color-primary-soft)', color: 'var(--color-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
                                        {review.username.charAt(0).toUpperCase()}
                                    </div>
                                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                                        <span className="reviewer-name">{review.username}</span>
                                        {review.is_buyed && (
                                            <span className="buyer-badge">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                                Doğrulanmış Satın Alım
                                            </span>
                                        )}
                                    </div>
                                </div>
                                <p className="review-text">{review.message}</p>
                            </div>
                        ))
                    )}
                </div>
            </div>
            {onerilenUrunler.length > 0 && (
                <div className="recommended-section">
                    <h3 className="reviews-header">İlginizi Çekebilecek Benzer Ürünler</h3>
                    <div style={{ display: 'flex', gap: '20px', overflowX: 'auto', padding: '10px 0' }}>
                        {onerilenUrunler.map((urun) => (
                            <div
                                key={urun.id}
                                className="product-card"
                                onClick={() => navigate(`/urunSayfasi/${urun.id}`)}
                                style={{ minWidth: '220px', maxWidth: '220px' }}
                            >
                                <div className="product-card__image-wrap">
                                    <img src={urun.photo} alt={urun.name} className="product-card__image" />
                                </div>
                                <div className="product-card__body" style={{ padding: '1rem' }}>
                                    <h4 className="product-card__name" style={{ fontSize: '1.1rem', marginBottom: '0.2rem' }}>{urun.name}</h4>
                                    <span style={{ fontWeight: '800', color: 'var(--color-ink)' }}>{urun.price} ₺</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {!isSeller && (
                <div style={{ position: 'fixed', bottom: '30px', right: '30px', zIndex: 1000 }}>
                    {!isChatOpen ? (
                        <button className="chat-fab" onClick={() => setIsChatOpen(true)}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                            Satıcıya Soru Sor
                        </button>
                    ) : (
                        <div className="chat-window">
                            <div className="chat-header">
                                <div style={{ display: 'flex', flexDirection: 'column' }}>
                                    <span style={{ fontWeight: '700', fontSize: '1.1rem' }}>{product.seller_name}</span>
                                    <span style={{ fontSize: '0.75rem', opacity: 0.8, fontWeight: '500' }}>Canlı Destek</span>
                                </div>
                                <button
                                    onClick={() => setIsChatOpen(false)}
                                    style={{ background: 'none', border: 'none', color: 'white', fontSize: '24px', cursor: 'pointer', lineHeight: '1', width: '32px', height: '32px', borderRadius: '50%', backgroundColor: 'rgba(255,255,255,0.2)' }}
                                >
                                    ×
                                </button>
                            </div>

                            <div className="chat-body">
                                {mesajlar.length === 0 ? (
                                    <div style={{ textAlign: 'center', color: 'var(--color-ink-faint)', fontSize: '0.9rem', marginTop: '2rem' }}>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginBottom: '1rem', opacity: '0.5' }}><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                                        <p>Satıcıya ürünle ilgili sorularınızı sorabilirsiniz.</p>
                                    </div>
                                ) : (
                                    mesajlar.map((msg, index) => (
                                        <div
                                            key={index}
                                            style={{
                                                maxWidth: '85%',
                                                padding: '10px 14px',
                                                borderRadius: '16px',
                                                alignSelf: msg.bizimMi ? 'flex-end' : 'flex-start',
                                                backgroundColor: msg.bizimMi ? 'var(--color-primary)' : 'var(--color-surface)',
                                                color: msg.bizimMi ? '#fff' : 'var(--color-ink)',
                                                fontSize: '0.9rem',
                                                borderBottomRightRadius: msg.bizimMi ? '4px' : '16px',
                                                borderBottomLeftRadius: msg.bizimMi ? '16px' : '4px',
                                                border: msg.bizimMi ? 'none' : '1px solid var(--color-line)',
                                                boxShadow: 'var(--shadow-sm)'
                                            }}
                                        >
                                            {msg.icerik}
                                        </div>
                                    ))
                                )}
                            </div>

                            <form className="chat-form"
                                onSubmit={(e) => {
                                    e.preventDefault();
                                    if (mesajlar.length === 0 && isSeller === false) {
                                        alanolustur(e);
                                    } else if (mesajlar.length === 0 && isSeller === true) {
                                        alert("satıcılar müşteri mesajlaşma başlatmadan mesaj gönderemez")
                                    } else if (mesajlar.length > 0) {
                                        if (yeniMesaj.trim() === "") {
                                            alert("Mesaj boş bırakılamaz");
                                        } else {
                                            mesajGönder();
                                        }
                                    }
                                }}
                            >
                                <input
                                    type="text"
                                    value={yeniMesaj}
                                    onChange={(e) => setYeniMesaj(e.target.value)}
                                    placeholder="Mesajınızı yazın..."
                                    style={{ flex: 1, padding: '0.8rem 1rem', border: '1px solid var(--color-line)', borderRadius: 'var(--radius-full)', outline: 'none', fontSize: '0.9rem', background: 'var(--color-surface-hover)' }}
                                />
                                <button
                                    type="submit"
                                    style={{ backgroundColor: 'var(--color-primary)', color: 'white', border: 'none', borderRadius: 'var(--radius-full)', width: '42px', height: '42px', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', transition: 'all 0.2s', boxShadow: 'var(--shadow-md)' }}
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
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