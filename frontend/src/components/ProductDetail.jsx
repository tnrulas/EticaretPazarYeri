import React from 'react'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'

import { useDispatch } from 'react-redux'
import { addToCart } from '../store/CartSlice'
import '../style/Urundetay.css'

function UrunDetay() {
    const { id } = useParams()
    const [product, setProduct] = useState(null)
    const [message, setMessage] = useState(null)

    const dispatch = useDispatch();

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await api.get(`urunler/Urunliste/${id}/`)
                setProduct(response.data)
            } catch (error) {
                console.error("Ürün detayları çekilirken hata oluştu:", error)
            }
        }
        fetchProduct();
    }, [id])

    useEffect(() => {
        const fetchReviews = async () => {

        }
    }, [])

    const handleAddReview = () => {

    }

    const handleAddToCart = () => {
        dispatch(addToCart(product));
        alert(`${product.name} sepete eklendi!`);
    }

    return (
        <div className="product-detail">
            {product && (
                <div className="product-detail__layout">
                    <div className="product-detail__image-wrap">
                        <img className="product-detail__image" src={product.photo} alt={product.name} />
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
                    </div>
                </div>
            )}
            <form>
                <input
                    type='text'
                />
            </form>
        </div>
    )
}

export default UrunDetay