import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api'
import { useSelector, useDispatch } from 'react-redux';


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
        <div>
            <h1>Siparişlerim</h1>
            {orders.length === 0 ? (
                <h1>Listelenecek bir siparişiniz yok</h1>
            ) : (

                orders.map((order) => (
                    <div key={order.id} style={{ border: '2px solid black', margin: '20px', padding: '10px' }}>
                        <h3>Sipariş Numarası: #{order.id}</h3>


                        {order.items.map((item) => (
                            <div key={item.id} style={{ display: 'flex', gap: '20px', alignItems: 'center', backgroundColor: '#f9f9f9', padding: '15px', marginTop: '10px', borderRadius: '8px' }}>

                                <div style={{ width: '80px', height: '80px', borderRadius: '8px', overflow: 'hidden', border: '1px solid #ddd' }}>
                                    {item.product_photo ? (
                                        <img src={item.product_photo} alt={item.product_name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                                    ) : (
                                        <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#eee' }}>📦</div>
                                    )}
                                </div>

                                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '5px' }}>
                                    <span style={{ fontWeight: 'bold', fontSize: '16px' }}>{item.product_name}</span>
                                    <span style={{ color: 'gray', fontSize: '14px' }}>Adet: {item.quantity}</span>
                                </div>


                                <div>
                                    <strong style={{ fontSize: '18px', color: '#007bff' }}>

                                        {item.product_price} ₺
                                    </strong>
                                </div>

                            </div>
                        ))}

                    </div>
                ))
            )}
        </div>
    )
}

export default MyOrders;