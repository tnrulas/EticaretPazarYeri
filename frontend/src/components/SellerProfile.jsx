import React from "react";
import { useState, useEffect } from 'react';
import api from "../services/api";
import { useNavigate, useParams } from "react-router-dom";
import '../style/Productlist.css'

function Seller() {

    const navigate = useNavigate();
    const [allProducts, setAllProducts] = useState([])
    const [sellerProfile, setSellerProfile] = useState(null);
    const [favoriler, setFavoriler] = useState([])

    const { id } = useParams();

    useEffect(() => {
        const FetchProducts = async () => {
            try {
                const response = await api.get(`urunler/satici/${id}/`)
                setAllProducts(response.data)
                console.log("Satıcının Ürünleri:", response.data);
            } catch (error) {
                console.error("Satıcı ürünleri çekilirken hata oluştu:", error);
            }
        }
        FetchProducts();
    }, [id])

    useEffect(() => {
        const FetchSellerProfile = async () => {
            try {
                const res = await api.get(`accounts/satici/${id}/`)
                setSellerProfile(res.data);
                console.log("Satıcının bilgileri:", res.data);
            } catch (error) {
                console.error("Satıcı bilgileri çekilirken hata oluştu:", error);
            }
        }
        FetchSellerProfile();
    }, [id])

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

    return (
        <div style={{ maxWidth: '1200px', margin: '3rem auto', padding: '0 1.5rem' }}>
            {sellerProfile && (
                <div className="seller-profile-header">
                    <div className="seller-profile-avatar">
                        {sellerProfile.company_name ? sellerProfile.company_name.charAt(0).toUpperCase() : sellerProfile.username.charAt(0).toUpperCase()}
                    </div>
                    <div className="seller-profile-info">
                        <h1 className="seller-profile-name">
                            {sellerProfile.company_name || sellerProfile.username}
                            <span className="seller-profile-badge">Resmi Mağaza</span>
                        </h1>
                        <div className="seller-profile-details">
                            <span className="seller-profile-detail-item">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                                <strong>Satıcı:</strong> {sellerProfile.username}
                            </span>
                            {sellerProfile.company_phone && (
                                <span className="seller-profile-detail-item">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                                    <strong>İletişim:</strong> {sellerProfile.company_phone}
                                </span>
                            )}
                            {sellerProfile.company_address && (
                                <span className="seller-profile-detail-item">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                                    <strong>Adres:</strong> {sellerProfile.company_address}
                                </span>
                            )}
                        </div>
                    </div>
                </div>
            )}

            <h2 className="seller-products-title">Mağazanın Ürünleri</h2>

            <div className="catalog">
                {allProducts.length === 0 ? (
                    <p style={{ textAlign: 'center', padding: '50px 0', color: '#888', fontSize: '18px' }}>Bu mağazada henüz ürün bulunmuyor.</p>
                ) : (
                    <ul className="catalog__grid">
                        {allProducts.map((product) => {
                            const isFavorited = favoriler.includes(product.id);
                            return (
                                <li key={product.id} className="product-card" onClick={() => navigate(`/urunSayfasi/${product.id}`)}>
                                    <div className="product-card__image-wrap">
                                        <img
                                            className="product-card__image"
                                            src={product.photo}
                                            alt={product.name}
                                        />
                                        <span className="product-card__price-badge">{product.price} ₺</span>

                                        <button
                                            className={`product-card__favorite-btn ${isFavorited ? 'active' : ''}`}
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                addFavorites(product.id)
                                            }}
                                            title="Favorilere Ekle"
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                viewBox="0 0 24 24"
                                                width="20"
                                                height="20"
                                                fill={isFavorited ? "#F43F5E" : "none"}
                                                stroke={isFavorited ? "#F43F5E" : "#475569"}
                                                strokeWidth="2"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                            >
                                                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                                            </svg>
                                        </button>
                                    </div>

                                    <div className="product-card__body">
                                        <h2 className="product-card__name">{product.name}</h2>
                                        <p className="product-card__description">{product.description}</p>

                                        <div className="product-card__meta">
                                            <span className="product-card__seller">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                                                {product.seller_name || sellerProfile?.username}
                                            </span>
                                            <span className="product-card__stock">Stok: {product.stock_count}</span>
                                        </div>

                                        <div className="product-card__cta-area">
                                            <button className="product-card__cta">Ürüne Git</button>
                                        </div>
                                    </div>
                                </li>
                            )
                        })}
                    </ul>
                )}
            </div>
        </div>
    )
}

export default Seller