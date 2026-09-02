import React from 'react'
import UrunOlustur from '../components/CreateProductForm'
import Navbar from '../components/Navbar'
import Footers from '../components/Footer'

function UrunOlusturSayfasi() {
    return (
        <div>
            <Navbar />
            <UrunOlustur />
            <Footers />
        </div>
    )
}

export default UrunOlusturSayfasi