import React from "react";
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from "react";
import api from '../services/api'
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../services/constants'
import { jwtDecode } from "jwt-decode"
import '../style/Profile.css'


function Profiles() {
    const navigate = useNavigate();
    const [reviews, setReviews] = useState([])
    const [user, setUser] = useState(null);
    const [adres, setAdres] = useState([])
    const [ziyaretler, setZiyaretler] = useState([])

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await api.get('urunler/yorumlarim/');
                setReviews(response.data);
            } catch (error) {
                console.error("Yorumlar çekilirken hata oluştu:", error);
            }
        };
        fetchReviews();
    }, []);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await api.get('accounts/listele/')
                console.log('KATEGORİLER:', response.data)
                setUser(response.data)
            } catch (error) {
                console.error("KUllanıcı çekilirken bir hata oluştu:", error)
            }
        }
        fetchUser();
    }, [])

    useEffect(() => {
        const fetchAddress = async () => {
            try {
                const response = await api.get('siparisler/adres/liste/')
                console.log("ADRESLER:", response.data)
                setAdres(response.data)
            } catch (error) {
                console.error("adres çekilirken bir hata oluştu:", error)
            }
        }
        fetchAddress();
    }, [])

    useEffect(() => {
        const fetchZiyaretler = async () => {
            try {
                const response = await api.get('urunler/ziyaret/liste/')
                setZiyaretler(response.data)
            } catch (error) {
                console.error("Ziyaret edilenler çekilirken hata oluştu:", error)
            }
        }
        fetchZiyaretler();
    }, [])

    const cikisYap = () => {
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        localStorage.removeItem('is_seller');
        navigate("/giris");
    }

    return (
        <div className="profile">
            {user && (
                <header className="profile__hero">
                    <div className="profile__avatar">{user.username.charAt(0).toUpperCase()}</div>
                    <div className="profile__hero-info">
                        <h1 className="profile__name">{user.username}</h1>
                        <p className="profile__email">{user.email}</p>
                    </div>
                    <button className="profile__logout" onClick={cikisYap}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                        Çıkış Yap
                    </button>
                </header>
            )}
            <div className="profile__quick">
                <button className="quick-tile" onClick={() => navigate("/siparislerim")}>
                    <span className="quick-tile__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                    </span>
                    <span className="quick-tile__text">
                        <strong>Siparişlerim</strong>
                        <small>Tüm siparişlerini görüntüle</small>
                    </span>
                    <span className="quick-tile__arrow">›</span>
                </button>

                <button className="quick-tile" onClick={() => navigate("/favoriler")}>
                    <span className="quick-tile__icon quick-tile__icon--heart">
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
                    </span>
                    <span className="quick-tile__text">
                        <strong>Favorilerim</strong>
                        <small>Beğendiğin ürünler</small>
                    </span>
                    <span className="quick-tile__arrow">›</span>
                </button>
            </div>

            {ziyaretler.length > 0 && (
                <section className="profile-card">
                    <h2 className="profile-card__title">Daha Önce Ziyaret Ettiklerim</h2>
                    <div className="visited-strip">
                        {ziyaretler.map((z) => (
                            <div key={z.id} className="visited-item" onClick={() => navigate(`/urunSayfasi/${z.product}`)}>
                                <div className="visited-item__img">
                                    <img src={z.product_photo} alt={z.product_name} />
                                </div>
                                <span className="visited-item__name">{z.product_name}</span>
                                <span className="visited-item__price">{z.product_price} ₺</span>
                            </div>
                        ))}
                    </div>
                </section>
            )}

            <div className="profile__grid">
                <section className="profile-card">
                    <h2 className="profile-card__title">İncelemelerim</h2>
                    {reviews.length === 0 ? (
                        <p className="profile-empty">Henüz bir değerlendirme yapmadın.</p>
                    ) : (
                        <ul className="review-list">
                            {reviews.map((r) => (
                                <li key={r.id} className="review-row" onClick={() => navigate(`/urunSayfasi/${r.product}`)}>
                                    <img className="review-row__img" src={r.product_photo} alt={r.product_name} />
                                    <div className="review-row__body">
                                        <div className="review-row__top">
                                            <strong>{r.product_name}</strong>
                                            <small>{new Date(r.created_at).toLocaleDateString('tr-TR')}</small>
                                        </div>
                                        <span className="review-row__stars">
                                            {'★'.repeat(r.rating)}
                                            <span className="review-row__stars--empty">{'★'.repeat(5 - r.rating)}</span>
                                        </span>
                                        {r.message && <p className="review-row__text">{r.message}</p>}
                                    </div>
                                </li>
                            ))}
                        </ul>
                    )}
                </section>

                <div className="profile__side">
                    {user && (
                        <section className="profile-card">
                            <h2 className="profile-card__title">Kullanıcı Bilgileri</h2>
                            <dl className="info-list">
                                <div className="info-row">
                                    <dt>Kullanıcı adı</dt>
                                    <dd>{user.username}</dd>
                                </div>
                                <div className="info-row">
                                    <dt>E-posta</dt>
                                    <dd>{user.email}</dd>
                                </div>
                                {(user.first_name || user.last_name) && (
                                    <div className="info-row">
                                        <dt>Ad Soyad</dt>
                                        <dd>{user.first_name} {user.last_name}</dd>
                                    </div>
                                )}
                            </dl>
                        </section>
                    )}

                    <section className="profile-card">
                        <h2 className="profile-card__title">Adres Bilgileri</h2>
                        {adres.length === 0 ? (
                            <p className="profile-empty">Kayıtlı adresin yok.</p>
                        ) : (
                            <ul className="address-list">
                                {adres.map((a) => (
                                    <li key={a.id} className="address-item">
                                        <strong>{a.city}</strong>
                                        <span>{a.street}</span>
                                        <small>{a.zip_code}</small>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </section>
                </div>
            </div>
        </div>
    )
}


export default Profiles