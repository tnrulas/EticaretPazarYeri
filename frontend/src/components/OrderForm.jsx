import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api'
import { useSelector, useDispatch } from 'react-redux';

function OrderForm() {
    const dispatch = useDispatch();

    const [address, setAddress] = useState({
        street: '',
        city: '',
        zip_code: ''
    });
    const [quantity, setQuantity] = useState(1);
    const navigate = useNavigate();

    const cartItems = useSelector((state) => state.cart.cartItems);


    const acceptPayment = async (e) => {
        e.preventDefault();

        if (cartItems.length === 0) {
            alert("Sepetiniz boş. Lütfen önce ürün ekleyin.");
            return;
        }
        try {
            const res = await api.post('siparisler/adres/ekle', address);
            const newAddressId = res.data.id;

            if (res.status === 200) {
                alert("Ödeme başarılı!");
            }

            const formattedItems = cartItems.map(item => ({
                product: item.id,
                quantity: item.quantity
            }));

            const payload = {
                address: newAddressId,
                items: formattedItems
            };

            const orderRes = await api.post('siparisler/olustur/', payload);

            if (orderRes.status === 201 || orderRes.status === 200) {
                alert("Ödeme alındı ve Sipariş başarıyla oluşturuldu!");
                setAddress({ street: '', city: '', zip_code: '' });

                navigate('/');
            }
        } catch (error) {
            console.error("İşlem sırasında hata oluştu:", error);
            alert("Bir hata oluştu, lütfen bilgilerinizi kontrol edin.");
        }
    }

    return (
        <div>
            <h1>Payment</h1>
            <form onSubmit={acceptPayment}>
                <div>
                    <label type="text">
                    </label>
                    <label>Adress street:</label>
                    <input
                        type="text"
                        value={address.street}
                        onChange={(e) => {
                            setAddress({
                                ...address,
                                street: e.target.value
                            })
                        }}
                    />
                    <label>Adress city:</label>
                    <input
                        type="text"
                        value={address.city}
                        onChange={(e) => {
                            setAddress({
                                ...address,
                                city: e.target.value
                            })
                        }}
                    />
                    <label>Adress zip:
                        <input
                            type="text"
                            value={address.zip_code}
                            onChange={(e) => {
                                setAddress({ ...address, zip_code: e.target.value })
                            }} />
                    </label>

                    <button type="submit">Ödeme Yap</button>
                </div>
            </form>
        </div>
    )
}

export default OrderForm;
