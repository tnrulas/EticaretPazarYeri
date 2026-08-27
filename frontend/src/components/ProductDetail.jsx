import React from 'react'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'

import { useDispatch } from 'react-redux'
import { addToCart } from '../store/CartSlice'
import '../style/Urundetay.css'

function UrunDetay() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);

    const [reviews, setReviews] = useState([]);
    const [newReviewText, setNewReviewText] = useState("");
    const [rating, setRating] = useState(5);

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

        </div>
    )
}

export default UrunDetay