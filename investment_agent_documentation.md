# Dokumentácia úprav Interest Bota na Investment Advisora

## 1. Popis provedených úprav

### Pôvodná funkcionalita (Interest Bot)
- Výpočet mesačných splátok pôžičiek
- Výpočet celkového úroku
- Základné finančné koncepty

### Nová funkcionalita (Investment Advisor)
- Výpočet zloženého úroku pre investície
- Analýza rizika portfólia
- Porovnanie rôznych investičných možností
- Odporúčania pre alokáciu aktív
- Vysvetlenie investičných konceptov

### Kľúčové zmeny v kóde

1. **Nové nástroje (tools)**
```python
def calculate_compound_interest(principal: float, rate: float, years: int) -> Dict:
    """Calculate compound interest and growth."""
    final_amount = principal * (1 + rate) ** years
    return {"final_amount": round(final_amount, 2), ...}

def calculate_portfolio_risk(equities: float, bonds: float, cash: float) -> Dict:
    """Calculate portfolio risk based on asset allocation."""
    risk_score = (equities * 0.8 + bonds * 0.3 + cash * 0.1) / 100
    return {"risk_score": round(risk_score, 2), ...}

def compare_investment_options(amount: float, years: int) -> Dict:
    """Compare different investment options."""
    returns = {
        "savings_account": 0.02,
        "bonds": 0.04,
        "stocks": 0.08,
        "real_estate": 0.06
    }
```

2. **Vylepšený systémový prompt**
```python
sys_msg = SystemMessage(content="""You are an investment advisor assistant. You can:
1. Calculate compound interest and investment growth
2. Analyze portfolio risk based on asset allocation
3. Compare different investment options
4. Provide investment recommendations
5. Explain investment concepts and strategies
""")
```

## 2. Ukážka vylepšených odpovedí

### Pred úpravou (Interest Bot)
```
User: Calculate returns for $50,000
Bot: Let me calculate that for you.
Monthly payment: $500
Total interest: $10,000
```

### Po úprave (Investment Advisor)
```
User: Porovnaj investičné možnosti pre 100 000 na 10 rokov.
Assistant: Tu sú rôzne investičné možnosti pre vašu investíciu 100 000 na 10 rokov:

1. Sporiaci účet (nízke riziko):
   - Konečná suma: 121 899,44
   - Celkový výnos: 21 899,44
   - Ročný výnos: 2%

2. Obligácie (stredné riziko):
   - Konečná suma: 148 024,43
   - Celkový výnos: 48 024,43
   - Ročný výnos: 4%

3. Akcie (vyššie riziko):
   - Konečná suma: 215 892,5
   - Celkový výnos: 115 892,5
   - Ročný výnos: 8%

Odporúčanie:
- 50% v akciách pre rast
- 30% v obligáciách pre stabilitu
- 10% v nehnuteľnostiach pre diverzifikáciu
- 10% na sporiacom účte pre likviditu
```

### Príklad analýzy rizika
```
User: Aké je riziko portfólia s 70% akcií, 20% obligácií a 10% hotovosti?
Assistant: Riziko vášho portfólia je hodnotené ako vysoké s rizikovým skóre 0.63. 

- 70% v akciách (vysoké riziko)
- 20% v obligáciách (stredné riziko)
- 10% v hotovosti (nízke riziko)
```

### Príklad vysvetlenia konceptov
```
User: Vysvetli mi, čo je to diverzifikácia portfólia.
Assistant: Diverzifikácia portfólia je investičná stratégia, ktorá spočíva v rozložení investícií do rôznych typov aktív s cieľom znížiť riziko. Predstavte si to ako príslovie "nedávaj všetky vajcia do jedného košíka".

Ak by ste napríklad investovali všetky svoje peniaze do jednej akcie a táto akcia by sa náhle zrútila, stratili by ste veľkú časť alebo všetky svoje investície. Ale ak by ste svoje peniaze rozložili medzi rôzne akcie, dlhopisy, hotovosť, nehnuteľnosti a iné typy aktív, pokles hodnoty jednej akcie by mal na celkové portfólio menší vplyv.
```

## 3. Screenshoty úprav kódu

### Nové nástroje
![Nové nástroje](tools_screenshot.png)
```python
tools = [
    calculate_compound_interest,
    calculate_portfolio_risk,
    compare_investment_options
]
```

### Vylepšený systémový prompt
![Systémový prompt](prompt_screenshot.png)
```python
sys_msg = SystemMessage(content="""You are an investment advisor assistant...""")
```

## 4. Zhrnutie vylepšení

1. **Rozšírená funkcionalita**
   - Pridaná analýza rizika portfólia
   - Porovnanie rôznych investičných možností
   - Výpočty zloženého úroku
   - Odporúčania pre alokáciu aktív

2. **Vylepšené odpovede**
   - Detailnejšie vysvetlenia
   - Kontextové odporúčania
   - Vyvážené investičné rady
   - Zrozumiteľné príklady

3. **Nové nástroje**
   - Kalkulácia rizika portfólia
   - Porovnávanie investičných možností
   - Výpočty zloženého úroku

4. **Lepšie promptovanie**
   - Kontextové otázky
   - Detailnejšie vysvetlenia
   - Praktické príklady
   - Zohľadnenie rizikových preferencií 