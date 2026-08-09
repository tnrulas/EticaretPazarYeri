import React from 'react'
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

function SepetListesi() {
    const navigate = useNavigate();

    const cartItems = useSelector((state) => state.cart.cartItems) || [];

    const toplamFiyat = cartItems.reduce((acc, urun) => {
        return acc + (parseFloat(urun.price) * (urun.quantitiy) || 1)
    }, 0);

    return (
        <div>
            <ul>
                {cartItems.map((ürün) => (
                    <li key={ürün.id}>
                        {ürün.name} - {ürün.price} ₺ (Adet: {ürün.quantity})
                    </li>
                ))}
            </ul>
            <h3>Toplam Fiyat: {toplamFiyat} ₺</h3>

            <button
                onClick={() => navigate('/odeme')}
                disabled={cartItems.length === 0}
            >
                Ödeme Ekranına Git
            </button>
        </div>
    )
}

export default SepetListesi