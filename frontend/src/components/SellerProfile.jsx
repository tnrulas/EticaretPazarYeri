import React from "react";
import { useState, useEffect } from 'react';
import api from "../services/api";
import { useNavigate, useParams } from "react-router-dom";
import '../style/Productlist.css'

function Seller() {

    const navigate = useNavigate();
    const [allProducts, setAllProducts] = useState([])
    const [sellerProfile, setSellerProfile] = useState(null);

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

    return (
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>


            {sellerProfile && (
                <div style={{
                    backgroundColor: '#f8f9fa',
                    borderRadius: '12px',
                    padding: '30px',
                    marginBottom: '30px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '20px',
                    border: '1px solid #eee',
                    boxShadow: '0 4px 6px rgba(0,0,0,0.05)'
                }}>


                    <div style={{
                        width: '100px',
                        height: '100px',
                        borderRadius: '50%',
                        backgroundColor: '#ff9900', // Turuncu E-Ticaret Rengi
                        color: 'white',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '36px',
                        fontWeight: 'bold',
                        flexShrink: 0
                    }}>
                        {sellerProfile.company_name ? sellerProfile.company_name.charAt(0).toUpperCase() : sellerProfile.username.charAt(0).toUpperCase()}
                    </div>


                    <div style={{ flex: '1' }}>
                        <h1 style={{ margin: '0 0 10px 0', fontSize: '28px', color: '#333' }}>
                            {sellerProfile.company_name || sellerProfile.username}
                            <span style={{ fontSize: '14px', backgroundColor: '#28a745', color: 'white', padding: '4px 8px', borderRadius: '4px', marginLeft: '10px', verticalAlign: 'middle' }}>Resmi Mağaza</span>
                        </h1>

                        <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', color: '#666', fontSize: '14px' }}>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                👤 <strong>Satıcı:</strong> {sellerProfile.username}
                            </span>

                            {sellerProfile.company_phone && (
                                <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                    📞 <strong>İletişim:</strong> {sellerProfile.company_phone}
                                </span>
                            )}

                            {sellerProfile.company_address && (
                                <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                    📍 <strong>Adres:</strong> {sellerProfile.company_address}
                                </span>
                            )}
                        </div>
                    </div>
                </div>
            )}




            <h2 style={{ borderBottom: '2px solid #ff9900', paddingBottom: '10px', marginBottom: '20px' }}>Mağazanın Ürünleri</h2>

            <div className="catalog">
                {allProducts.length === 0 ? (
                    <p style={{ textAlign: 'center', padding: '50px 0', color: '#888', fontSize: '18px' }}>Bu mağazada henüz ürün bulunmuyor.</p>
                ) : (
                    <ul className="catalog__grid">
                        {allProducts.map((product) => {
                            return (
                                <li key={product.id} className="product-card">
                                    <div className="product-card__image-wrap">
                                        <img
                                            className="product-card__image"
                                            src={product.photo}
                                            alt={product.name}
                                        />
                                        <span className="product-card__price">{product.price} ₺</span>
                                    </div>
                                    <div className="product-card__body">
                                        <h2 className="product-card__name">{product.name}</h2>
                                        <p className="product-card__description">{product.description}</p>
                                        <div className="product-card__meta">

                                            <span className="product-card__seller">Satıcı: {product.seller_name || sellerProfile?.username}</span>
                                            <span className="product-card__stock">Stok: {product.stock_count}</span>
                                        </div>
                                        <button
                                            className="product-card__cta"
                                            onClick={() => navigate(`/urunSayfasi/${product.id}`)}
                                        >
                                            Ürüne git
                                        </button>
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