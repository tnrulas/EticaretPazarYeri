import React from 'react'
import { useState, useEffect } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';
import '../style/Urunolustur.css'

function UrunOlustur() {
    const navigate = useNavigate();

    const [urunIsmi, setUrunIsmi] = useState('');
    const [urunAciklamasi, setUrunAciklamasi] = useState('');
    const [urunResmi, setUrunResmi] = useState(null);
    const [urunFiyati, setUrunFiyati] = useState('');
    const [stokSayisi, setStokSayisi] = useState('');

    const olustur = async (e) => {
        e.preventDefault();

        try {
            const isSeller = localStorage.getItem('is_seller');
            if (isSeller !== 'true') {
                alert('Ürün oluşturmak için satıcı olmanız gerekmektedir.');
                return;
            }
            const formData = new FormData();
            formData.append('name', urunIsmi);
            formData.append('description', urunAciklamasi);
            formData.append('price', urunFiyati);
            formData.append('stock_count', stokSayisi);

            if (urunResmi) {
                formData.append('photo', urunResmi);
            }

            const res = await api.post('urunler/Urunekle/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert('Ürün başarı ile oluşturuldu!');

            navigate("/")

        } catch (error) {
            if (error.response && error.response.data) {
                console.error("Django'nun reddetme sebebi:", error.response.data);
                alert(`Kayıt Başarısız!\nSebep: ${JSON.stringify(error.response.data)}`);
            } else {
                console.error("Ürün oluşturulurken hata oluştu.", error);
                alert("İşlem başarısız oldu. Sunucuya ulaşılamıyor.");
            }
        } finally {
            setUrunIsmi('');
            setUrunAciklamasi('');
            setUrunResmi(null);
            setUrunFiyati('');
            setStokSayisi('');
        }
    }

    return (
        <div className="product-form">
            <div className="product-form__card">
                <p className="product-form__eyebrow">Satıcı paneli</p>
                <h1 className="product-form__title">Ürün Oluştur</h1>
                <form className="product-form__form" onSubmit={(e) => { olustur(e); }}>
                    <div className="product-form__field">
                        <label>Ürün İsmi</label>
                        <input type="text" value={urunIsmi} onChange={(e) => setUrunIsmi(e.target.value)} required />
                    </div>
                    <div className="product-form__field">
                        <label>Açıklama</label>
                        <textarea
                            value={urunAciklamasi}
                            onChange={(e) => setUrunAciklamasi(e.target.value)}
                            required
                        />
                    </div>

                    <div className="product-form__row">
                        <div className="product-form__field">
                            <label>Fiyat (₺)</label>
                            <input
                                type="number"
                                value={urunFiyati}
                                onChange={(e) => setUrunFiyati(e.target.value)}
                                required
                            />
                        </div>

                        <div className="product-form__field">
                            <label>Stok Sayısı</label>
                            <input
                                type="number"
                                value={stokSayisi}
                                onChange={(e) => setStokSayisi(e.target.value)}
                                required
                            />
                        </div>
                    </div>

                    <div className="product-form__field product-form__field--file">
                        <label>Ürün Resmi</label>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={(e) => setUrunResmi(e.target.files[0])}
                        />
                    </div>
                    <button type="submit" className="product-form__submit">Ürün Oluştur</button>
                </form>
            </div>
        </div>
    )
}

export default UrunOlustur
