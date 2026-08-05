import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';


function OrderForm() {
    const [address, setAddress] = useState([]);


    const acceptPayment = () => {

    }

    return (
        <div>
            <h1>Payment</h1>
            <form>
                <div>
                    <label type="text">
                    </label>
                    <button onClick={acceptPayment}>Ödeme Yap</button>
                </div>
            </form>
        </div>
    )
}
