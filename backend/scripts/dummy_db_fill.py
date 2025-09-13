import sqlite3

DATABASE_NAME = "Parking.db"


def fill_discount_rule(cursor):
    """Fill discount_rule table with example records"""
    discount_rules = [
        (1, 'WEEKEND10', 'PERCENT', 10, '2025-09-12T00:00:00', '2025-09-15T00:00:00'),
        (2, 'LOYALTY5', 'FIXED', 500, None, None)
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO discount_rule (id, code, kind, value, valid_from, valid_to)
        VALUES (?, ?, ?, ?, ?, ?)
    """, discount_rules)
    print("Filled discount_rule table with 3 records")


def fill_payment(cursor):
    """Fill payment table with example records"""
    payments = [
        (1, 45, 3, 'card', 5000, 1, 'TXN-ABCD123', '2025-09-09T14:35:00'),
        (2, 46, 4, 'cash', 3000, 1, None, '2025-09-09T15:12:00'),
        (3, 47, 5, 'online', 4500, 0, 'TXN-XYZ789', '2025-09-09T15:30:00')
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO payment (id, session_id, station_id, method, amount_cents, approved, processor_ref, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, payments)
    print("Filled payment table with 3 records")


def fill_voucher(cursor):
    """Fill voucher table with example records"""
    vouchers = [
        (1, 'FREEPARK2025', 0, '2025-06-30T23:59:59'),
        (2, 'GIFT-50MDL', 5000, None),
        (3, 'EVENTPASS123', 2000, '2025-09-30T23:59:59')
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO voucher (id, code, balance_cents, expires_at)
        VALUES (?, ?, ?, ?)
    """, vouchers)
    print("Filled voucher table with 3 records")


def fill_tariff(cursor):
    """Fill tariff table with example records"""
    tariffs = [
        (1, 'Standard Tariff', 15, 500, 6000),
        (2, 'Weekend Special', 30, 300, 4000),
        (3, 'VIP Customers', 60, 0, 0)
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO tariff (id, name, free_minutes, rate_cents_per_hour, max_daily_cents)
        VALUES (?, ?, ?, ?, ?)
    """, tariffs)
    print("Filled tariff table with 3 records")


def fill_station(cursor):
    """Fill station table with example records"""
    stations = [
        (1, 1, 'entry_terminal', 'Entry Lane A'),
        (2, 1, 'exit_terminal', 'Exit Lane A'),
        (3, 2, 'pof', 'POF-01')
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO station (id, zone_id, kind, label)
        VALUES (?, ?, ?, ?)
    """, stations)
    print("Filled station table with 3 records")


def fill_ticket(cursor):
    """Fill ticket table with example records"""
    tickets = [
        (1, 'TCK-20250909-12345', '2025-09-09T08:15:00', 1, 'active'),
        (2, 'TCK-20250908-54321', '2025-09-08T19:00:00', 2, 'paid'),
        (3, 'TCK-20250907-11111', '2025-09-07T10:30:00', 1, 'lost')
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO ticket (id, code, issued_at, entry_station, status)
        VALUES (?, ?, ?, ?, ?)
    """, tickets)
    print("Filled ticket table with 3 records")


def fill_session(cursor):
    """Fill session table with example records"""
    sessions = [
        (1, 1234, '2025-09-09T08:15:00', 1, '2025-09-09T12:45:00', 2, 'exited', 3000, 3000, '2025-09-09T12:50:00', 'ABC123', 'ABC123'),
        (2, 1235, '2025-09-09T09:00:00', 1, None, None, 'active', 1500, 0, None, 'XYZ999', None),
        (3, None, '2025-09-09T10:30:00', 1, None, None, 'active', 0, 0, None, 'DEF777', None)
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO session (id, ticket_id, entry_time, entry_station, exit_time, exit_station, status, amount_due_cents, amount_paid_cents, paid_until, licence_plate_entry, licence_plate_exit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sessions)
    print("Filled session table with 3 records")


def fill_event(cursor):
    """Fill event table with example records"""
    events = [
        (1, 101, 1, 'TICKET_ISSUED', '2025-09-09T08:15:00', '{"ticket_code": "TCK-12345"}'),
        (2, 101, 5, 'ANPR_READ', '2025-09-09T08:15:05', '{"plate": "ABC123", "confidence": 0.93}'),
        (3, 101, 3, 'PAYMENT_OK', '2025-09-09T12:40:00', '{"amount_cents": 3000, "method": "card"}'),
        (4, 101, 2, 'BARRIER_RAISE', '2025-09-09T12:45:00', '{"trigger": "session_paid"}')
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO event (id, session_id, station_id, type, occurred_at, payload_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, events)
    print("Filled event table with 4 records")


def fill():
    """Main function to fill all tables with example data"""
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    
    try:
        print("Starting to fill database with example records...")
        
        # Fill all tables in dependency order
        fill_discount_rule(cursor)
        fill_voucher(cursor)
        fill_tariff(cursor)
        fill_station(cursor)
        fill_ticket(cursor)
        fill_session(cursor)
        fill_payment(cursor)
        fill_event(cursor)
        
        connection.commit()
        print("\n✅ Successfully filled all tables with example data!")
        
    except Exception as e:
        print(f"❌ Error filling database: {e}")
        connection.rollback()
    finally:
        connection.close()


if __name__ == "__main__":
    fill()
