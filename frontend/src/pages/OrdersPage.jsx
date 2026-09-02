import React from "react";
import Navbar from '../components/Navbar'
import MyOrders from "../components/Orders";
import Footers from '../components/Footer'


function Order() {
    return (
        <div>
            <Navbar />
            <MyOrders />
            <Footers />
        </div>
    )
}

export default Order