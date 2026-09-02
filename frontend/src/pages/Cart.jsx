import React from 'react'
import SepetListesi from '../components/CartList'
import Navbar from '../components/Navbar'
import Footers from '../components/Footer'

function Sepet() {
    return (
        <div>
            <Navbar />
            <SepetListesi />
            <Footers />
        </div>
    )
}

export default Sepet