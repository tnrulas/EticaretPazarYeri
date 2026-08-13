import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api'
import { useSelector, useDispatch } from 'react-redux';
import '../style/Orederform.css'

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
            const res = await api.post('siparisler/adres/ekle/', address);
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

            const createdOrderId = orderRes.data.id;

            const paymentRes = await api.post(`fatura/odeme/ekle/${createdOrderId}/`, {});

            if (paymentRes === 201 || paymentRes.status === 200) {
                alert("Ödeme alındı, siparişiniz başarıyla doğrulandı!");


                setAddress({ street: '', city: '', zip_code: '' });
                navigate('/odemeBasarili');
            }

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
        <div className="checkout">
            <div className="checkout__card">
                <p className="checkout__eyebrow">Son adım</p>
                <h1 className="checkout__title">Ödeme</h1>
                <form className="checkout__form" onSubmit={acceptPayment}>
                    <div className="checkout__field">
                        <label>Adres (Sokak)</label>
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
                    </div>
                    <div className="checkout__field">
                        <label>Şehir</label>
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
                    </div>
                    <div className="checkout__field">
                        <label>Posta Kodu</label>
                        <input
                            type="text"
                            value={address.zip_code}
                            onChange={(e) => {
                                setAddress({ ...address, zip_code: e.target.value })
                            }} />
                    </div>

                    <button type="submit" className="checkout__submit">Ödeme Yap</button>
                </form>
            </div>
        </div>
    )
}

export default OrderForm;
