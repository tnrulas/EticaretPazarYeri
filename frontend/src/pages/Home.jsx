import React from 'react'
import ProductList from '../components/ProductList'
import Navbar from '../components/Navbar'
import Footers from '../components/Footer'

function Anasayfa() {
    return (
        <div>
            <Navbar />
            <ProductList />
            <Footers />
        </div>
    )
}

export default Anasayfa