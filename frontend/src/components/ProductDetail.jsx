import React from 'react'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'

import { useDispatch } from 'react-redux'
import { addToCart } from '../store/CartSlice'

function UrunDetay() {
    const { id } = useParams()
    const [product, setProduct] = useState(null)

    const dispatch = useDispatch();

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await api.get(`Urunliste/${id}/`)
                setProduct(response.data)
            } catch (error) {
                console.error("Ürün detayları çekilirken hata oluştu:", error)
            }
        }
        fetchProduct();
    }, [id])

    const handleAddToCart = () => {
        dispatch(addToCart(product));
        alert(`${product.name} sepete eklendi!`);
    }

    return (
        <div>
            {product && (
                <div>
                    <img src={product.photo} alt={product.name} />
                    <h2>{product.name}</h2>
                    <p>{product.description}</p>
                    <p>Fiyat: {product.price}</p>
                    <p>Satıcı: {product.seller}</p>
                    <p>Stock: {product.stock_count}</p>
                    <button onClick={handleAddToCart}>
                        Sepete Ekle
                    </button>
                </div>
            )}
        </div>
    )
}

export default UrunDetay