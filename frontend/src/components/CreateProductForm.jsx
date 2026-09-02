import React from 'react'
import { useState, useEffect } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';
import '../style/Urunolustur.css'

function UrunOlustur() {

    const categories = [
        "Elektronik", "Moda & Giyim", "Ev, Mobilya & Yaşam", "Kozmetik & Kişisel Bakım",
        "Anne, Bebek & Oyuncak", "Spor & Outdoor", "Süpermarket & Gıda", "Kitap, Müzik & Hobi",
        "Otomobil & Motosiklet", "Evcil Hayvan Ürünleri", "Ofis & Kırtasiye", "Saat, Takı & Aksesuar",
        "Ayakkabı & Çanta", "Yapı Market & Hırdavat", "Bahçe & Teras", "Oyun & Konsol",
        "Sağlık & Medikal Ürünler", "Müzik Aletleri", "Sanat, Hobi & El İşi"
    ];

    const navigate = useNavigate();

    const [urunIsmi, setUrunIsmi] = useState('');
    const [urunAciklamasi, setUrunAciklamasi] = useState('');
    const [urunResmi, setUrunResmi] = useState(null);
    const [urunFiyati, setUrunFiyati] = useState('');
    const [stokSayisi, setStokSayisi] = useState('');
    const [kategori, setKategori] = useState('')
    const [ekstraResim, setEkstraResim] = useState([])

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
            formData.append('category', kategori);

            if (urunResmi) {
                formData.append('photo', urunResmi);
            }

            if (ekstraResim) {
                for (let resim of ekstraResim) {
                    formData.append('images', resim)
                }
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
            setKategori('')
            setEkstraResim([]);
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
                        <label>Ürün Kapak Resmi</label>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={(e) => setUrunResmi(e.target.files[0])}
                        />
                    </div>

                    <div className="product-form__field product-form__field--file">
                        <label>Ürün diğer resimleri (Birden fazla seçebilirsiniz)</label>
                        <input
                            type="file"
                            accept="image/*"
                            multiple
                            onChange={(e) => setEkstraResim(Array.from(e.target.files))}
                        />
                    </div>

                    <div className="product-form__field product-form__field--file">
                        <label>Ürün kategorisi</label>
                        <select
                            value={kategori}
                            onChange={(e) => setKategori(e.target.value)}
                            required
                            style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
                        >
                            <option value="" disabled>Lütfen bir kategori seçin</option>
                            {categories.map((cat, index) => (
                                <option key={index} value={cat}>
                                    {cat}
                                </option>
                            ))}
                        </select>
                    </div>
                    <button type="submit" className="product-form__submit">Ürün Oluştur</button>
                </form>
            </div>
        </div>
    )
}

export default UrunOlustur
