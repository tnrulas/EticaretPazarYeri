import React from 'react'
import Navbar from '../components/Navbar'
import SearchAll from '../components/CategoryList'
import CategoryLists from '../components/CategoryList'

function Categories() {
    return (
        <div>
            <Navbar />
            <CategoryLists />
        </div>
    )
}

export default Categories