import React from 'react'
import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import '../style/Productlist.css'
import api from '../services/api';

function SearchAll() {
    const [products, setProducts] = useState([])
    const navigate = useNavigate();

    const [searchParams] = useSearchParams();
    const query = searchParams.get('q') || '';

    const [favoriler, setFavoriler] = useState([])

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await api.get('urunler/ara/', {
                    params: { q: query }
                })
                setProducts(response.data)
            } catch (error) {
                console.error("Ürünler çekilirken hata oluştu:", error)
            }
        }

        fetchProducts();
    }, [query])

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
        <div className="catalog">
            <div className="catalog__header">
                <p className="catalog__eyebrow">Pazar yeri</p>
                <h1 className="catalog__title">Ürünler ve Hizmetler</h1>
            </div>

            {products.length === 0 ? (
                <p className="catalog__empty">Şu anda listelenecek ürün yok.</p>
            ) : (
                <ul className="catalog__grid">
                    {products.map((product) => {
                        const isFavorited = favoriler.includes(product.id);
                        return (
                            <li key={product.id} className="product-card">
                                <div className="product-card__image-wrap" style={{ position: 'relative' }}>
                                    <img
                                        className="product-card__image"
                                        src={product.photo}
                                        alt={product.name}
                                    />
                                    <span className="product-card__price">{product.price} ₺</span>

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
                                            fill={isFavorited ? "#ff4757" : "none"}
                                            stroke={isFavorited ? "#ff4757" : "#636e72"}
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
                                        <span className="product-card__seller">Satıcı: {product.seller}</span>
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
    )
}

export default SearchAll