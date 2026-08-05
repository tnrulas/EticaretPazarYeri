import React from 'react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'


function ProductList() {
    const [products, setProducts] = useState([])
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await api.get('Urunliste/')
                setProducts(response.data)
            } catch (error) {
                console.error("Ürünler çekilirken hata oluştu:", error)
            }
        }

        fetchProducts();
    }, [])

    return (
        <div>
            <h1>Ürünler ve Hizmetler</h1>
            <ul>
                {products.map((product) => {
                    return (
                        <li key={product.id}>
                            <image src={product.photo}
                                alt={product.name} />
                            <h2>{product.name}</h2>
                            <p>{product.description}</p>
                            <p>Fiyat: {product.price}</p>
                            <h2>Satıcı: {product.seller}</h2>
                            <p>Stok: {product.stock_count}</p>
                            <button onClick={() => {
                                navigate(`/Urun/${product.id}`)
                            }}>Ürüne git</button>
                        </li>
                    )
                })}
            </ul>
        </div>
    )
}

export default ProductList