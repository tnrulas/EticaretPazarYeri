import React from 'react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import '../style/Productlist.css'


function Fav() {
    const [products, setProducts] = useState([])
    const [productImage, setProductImage] = useState([])
    const [favoriler, setFavoriler] = useState([])
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await api.get('accounts/favorilerim/')
                setProducts(response.data)
            } catch (error) {
                console.error("Ürünler çekilirken hata oluştu:", error)
            }
        }

        fetchProducts();
    }, [])

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
                <h1 className="catalog__title">Favorilerim</h1>
            </div>

            {products.length === 0 ? (
                <p className="catalog__empty">Şu anda listelenecek ürün yok.</p>
            ) : (
                <ul className="catalog__grid">
                    {products.map((product) => {
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
                                            {product.seller}
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
    )
}

export default Fav