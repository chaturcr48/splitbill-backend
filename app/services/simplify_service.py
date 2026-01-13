from collections import defaultdict

def simplify_balances(raw_balances):
    net = defaultdict(float)

    for b in raw_balances:
        net[b["from_user"]] -= b["amount"]
        net[b["to_user"]] += b["amount"]

    debtors = []
    creditors = []

    for user, amount in net.items():
        if amount < 0:
            debtors.append([user, -amount])
        elif amount > 0:
            creditors.append([user, amount])

    i = j = 0
    simplified = []

    while i < len(debtors) and j < len(creditors):
        d_user, d_amt = debtors[i]
        c_user, c_amt = creditors[j]

        settle = min(d_amt, c_amt)

        simplified.append({
            "from_user": d_user,
            "to_user": c_user,
            "amount": round(settle, 2)
        })

        debtors[i][1] -= settle
        creditors[j][1] -= settle

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return simplified
