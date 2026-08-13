import React from 'react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import '../style/Productlist.css'


function ProductList() {
    const [products, setProducts] = useState([])
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await api.get('urunler/Urunliste/')
                setProducts(response.data)
            } catch (error) {
                console.error("Ürünler çekilirken hata oluştu:", error)
            }
        }

        fetchProducts();
    }, [])

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

export default ProductList