import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api'
import { useSelector, useDispatch } from 'react-redux';
import '../style/Orders.css';


function MyOrders() {
    const [orders, setOrders] = useState([])
    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const res = await api.get('siparisler/liste/')
                setOrders(res.data)
            } catch (error) {
                console.error('siparişler çekilemedi', error)
            }
        }
        fetchOrders();
    }, [])
    return (
        <div className="orders">
            <div className="orders__header">
                <h1 className="orders__title">Siparişlerim</h1>
            </div>
            {orders.length === 0 ? (
                <div className="orders__empty">Şu an verilmiş bir siparişiniz bulunmamaktadır.</div>
            ) : (
                orders.map((order) => (
                    <div key={order.id} className="order-card">
                        <div className="order-card__header">
                            <h3 className="order-card__id">Sipariş # {order.id}</h3>
                        </div>

                        <div className="order-card__items">
                            {order.items.map((item) => (
                                <div key={item.id} className="order-item">
                                    <div className="order-item__image-wrap">
                                        {item.product_photo ? (
                                            <img src={item.product_photo} alt={item.product_name} className="order-item__image" />
                                        ) : (
                                            <div className="order-item__placeholder">📦</div>
                                        )}
                                    </div>

                                    <div className="order-item__details">
                                        <span className="order-item__name">{item.product_name}</span>
                                        <span className="order-item__qty">Adet: {item.quantity}</span>
                                    </div>

                                    <div className="order-item__price">
                                        {item.product_price} ₺
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))
            )}
        </div>
    )
}

export default MyOrders;