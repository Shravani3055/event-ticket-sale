import streamlit as st
import hashlib
import time
import json

class Block:
    def __init__(self, index, timestamp, ticket_data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.ticket_data = ticket_data  # e.g., buyer, seat
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.ticket_data)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class TicketBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"event": "Concert A", "info": "Genesis Block"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_ticket_sale(self, buyer_name, seat_number):
        ticket_data = {
            "event": "Concert A",
            "buyer": buyer_name,
            "seat": seat_number
        }
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), ticket_data, latest_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True

    def get_chain_data(self):
        chain_data = []
        for block in self.chain:
            chain_data.append({
                "Block #": block.index,
                "Time": time.ctime(block.timestamp),
                "Ticket Info": block.ticket_data,
                "Hash": block.hash,
                "Prev Hash": block.previous_hash
            })
        return chain_data

# Streamlit UI

st.title("Ticket Blockchain")

# Initialize the blockchain
ticket_chain = TicketBlockchain()

# User input for new ticket sale
st.subheader("Add New Ticket Sale")
buyer_name = st.text_input("Enter Buyer's Name")
seat_number = st.text_input("Enter Seat Number")

if st.button("Add Ticket Sale"):
    if buyer_name and seat_number:
        ticket_chain.add_ticket_sale(buyer_name, seat_number)
        st.success(f"Ticket Sale Added for {buyer_name} with Seat {seat_number}")
    else:
        st.error("Please enter both buyer's name and seat number.")

# Show blockchain status
st.subheader("Current Blockchain")
if ticket_chain.chain:
    chain_data = ticket_chain.get_chain_data()
    st.write(chain_data)

# Validate the blockchain
st.subheader("Blockchain Validation")
if st.button("Validate Blockchain"):
    if ticket_chain.is_chain_valid():
        st.success("Blockchain is valid!")
    else:
        st.error("Blockchain has been tampered with!")

