import React from 'react'
import { useState, useEffect } from 'react';
import api from '../services/api';

function UrunOlustur() {

    const [urunIsmi, setUrunIsmi] = useState('');
    const [urunAciklamasi, setUrunAciklamasi] = useState('');
    const [urunResmi, setUrunResmi] = useState(null);
    const [urunFiyati, setUrunFiyati] = useState('');
    const [stokSayisi, setStokSayisi] = useState('');

    const olustur = async (e) => {
        e.preventDefault();

        try {
            const is_seller = localStorage.getItem('is_seller');
            if (is_seller !== 'true') {
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

        } catch (error) {
            console.error("Ürün oluşturulurken hata oluştu.", error);
        } finally {
            setUrunIsmi('');
            setUrunAciklamasi('');
            setUrunResmi(null);
            setUrunFiyati('');
            setStokSayisi('');
        }
    }

    return (
        <div>
            <h1>UrunOlustur</h1>
            <form onSubmit={(e) => { olustur(e); }}>
                <div>
                    <label>Ürün İsmi:</label>
                    <input type="text" value={urunIsmi} onChange={(e) => setUrunIsmi(e.target.value)} required />
                </div>
                <div>
                    <label>Açıklama:</label>
                    <textarea
                        value={urunAciklamasi}
                        onChange={(e) => setUrunAciklamasi(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Fiyat:</label>
                    <input
                        type="number"
                        value={urunFiyati}
                        onChange={(e) => setUrunFiyati(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Stok Sayısı:</label>
                    <input
                        type="number"
                        value={stokSayisi}
                        onChange={(e) => setStokSayisi(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Ürün Resmi:</label>
                    <input
                        type="file"
                        accept="image/*"

                        onChange={(e) => setUrunResmi(e.target.files[0])}
                    />
                </div>
                <button type="submit">Ürün Oluştur</button>
            </form>
        </div>
    )
}

export default UrunOlustur
