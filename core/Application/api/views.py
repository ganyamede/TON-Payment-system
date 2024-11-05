from datetime import datetime, timedelta
from flask import render_template, request, session, jsonify
from core.blockchain.payment_checker import (
    SaveWallet, 
    UpdateWallet, 
    ConnectWallet
)

from core.storage.database import Select

def HomeView():
    return render_template('index.html')

def PayView():
    """
    Handle the payment view logic. If the user's address is in the session,
    retrieve the stored values. Otherwise, process the payment details 
    and save them to the session.
    """
    if "address" in session:
        # Retrieve stored values from the session
        formatted_time = session['formatted_time']
        address = session['address']
        value = session['value']
    else:
        # Get payment value from the form and process it
        value = request.form.get('value')
        args = SaveWallet(value)
        print(args)
        address = args.wallet.address.to_str()
        
        # Set the formatted time for one hour from now
        new_time = datetime.now() + timedelta(hours=1)
        formatted_time = new_time.strftime("%H:%M") 

        # Store the values in the session
        session['formatted_time'] = formatted_time
        session['address'] = address
        session['value'] = value

    # Render the payment payload template with the relevant information
    return render_template('payload.html', address=address, value=value, formatted_time=formatted_time)

def CheckPay():
    """
    Check the payment status for a given address. Verify if the wallet 
    is connected and has enough balance to cover the payment amount.
    
    :return: JSON response indicating whether the payment can be processed.
    """
    # Get the address from the form data
    address = request.form.get('address')

    # Retrieve the payment details from the database
    result = Select('ton', columns='id, state, value', where_clause=f'address = "{address}"')
    result = result.execute()
    
    # Extract transaction details
    tid = result[0][0]  # Transaction ID
    state = result[0][1]  # Current state
    value = result[0][2]  # Payment value

    # Check the wallet's information
    Information = ConnectWallet(address=address)
    if Information.account_state and state == '0':
        print(state)
        # Check if the available balance is sufficient
        if int(Information.available_balance) >= int(value):
            UpdateWallet(tid)
        
        # Return a JSON response indicating success
        return jsonify(int(Information.available_balance) >= int(value))
    else:
        # Return a JSON response indicating failure
        return jsonify(False)
