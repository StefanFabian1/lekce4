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
- Validácia vstupov a spracovanie chýb
- Spracovanie extrémnych scenárov

### Kľúčové zmeny v kóde

1. **Nové nástroje (tools)**
```python
def calculate_compound_interest(principal: float, rate: float, years: int) -> Dict:
    """Calculate compound interest and growth."""
    validation = validate_inputs(principal=principal, rate=rate, years=years)
    if not validation["is_valid"]:
        return {"error": validation["errors"]}
    final_amount = principal * (1 + rate) ** years
    return {"final_amount": round(final_amount, 2), ...}

def calculate_portfolio_risk(equities: float, bonds: float, cash: float) -> Dict:
    """Calculate portfolio risk based on asset allocation."""
    validation = validate_inputs(equities=equities, bonds=bonds, cash=cash)
    if not validation["is_valid"]:
        return {"error": validation["errors"]}
    risk_score = (equities * 0.8 + bonds * 0.3 + cash * 0.1) / 100
    return {"risk_score": round(risk_score, 2), ...}

def compare_investment_options(amount: float, years: int) -> Dict:
    """Compare different investment options."""
    validation = validate_inputs(principal=amount, years=years)
    if not validation["is_valid"]:
        return {"error": validation["errors"]}
    returns = {
        "savings_account": 0.02,
        "bonds": 0.04,
        "stocks": 0.08,
        "real_estate": 0.06
    }
```

2. **Validácia vstupov**
```python
def validate_inputs(principal: float = None, rate: float = None, years: float = None, 
                   equities: float = None, bonds: float = None, cash: float = None) -> Dict:
    """Validate input parameters and return error messages if any."""
    errors = []
    
    if principal is not None and principal <= 0:
        errors.append("Výška investície musí byť kladné číslo.")
    
    if years is not None:
        if years <= 0:
            errors.append("Investičný horizont musí byť kladné číslo.")
        elif years < 0.1:  # Menej ako 1 mesiac
            errors.append("Minimálny investičný horizont je 1 mesiac.")
        elif years > 100:
            errors.append("Maximálny investičný horizont je 100 rokov.")
    
    # ... ďalšie validácie ...
    
    return {"is_valid": len(errors) == 0, "errors": errors}
```

3. **Vylepšený systémový prompt**
```python
sys_msg = SystemMessage(content="""You are an investment advisor assistant. You can:
1. Calculate compound interest and investment growth
2. Analyze portfolio risk based on asset allocation
3. Compare different investment options
4. Provide investment recommendations
5. Explain investment concepts and strategies

Always:
- Validate inputs and provide clear error messages
- Handle edge cases gracefully
- Explain why the input is invalid if needed
- Provide guidance on correct input format
- Suggest reasonable alternatives
""")
```

## 2. Testovanie a výsledky

### Testovanie "not happy day" scenárov

1. **Neplatné vstupy - záporné čísla**
```
User: Vypočítaj mi výnos z -50000€ pri 5% úroku
Assistant: Výška investície musí byť kladné číslo. Prosím, zadajte kladnú hodnotu.
```

2. **Neplatné vstupy - nesprávne percentá**
```
User: Aké je riziko portfólia s 120% akcií a -20% obligácií?
Assistant: Podiel akcií musí byť medzi 0% a 100%. Podiel obligácií musí byť medzi 0% a 100%.
```

3. **Neúplné informácie**
```
User: Chcem investovať peniaze
Assistant: Potrebujem vedieť:
1. Aká je suma, ktorú plánujete investovať?
2. Aký je váš investičný horizont?
3. Aká je vaša tolerancia k riziku?
```

4. **Extrémne scenáre - veľmi krátky horizont**
```
User: Aký bude výnos z 10000€ pri 5% úroku za 1 deň?
Assistant: Minimálny investičný horizont je 1 mesiac. Pre krátkodobé investície odporúčam sporiaci účet.
```

5. **Extrémne scenáre - veľmi dlhý horizont**
```
User: Porovnaj investície pre 50000€ na 100 rokov
Assistant: Maximálny investičný horizont je 100 rokov. Výpočty nezohľadňujú infláciu a iné faktory.
```

6. **Neočakávané požiadavky**
```
User: Ako sa varí guláš?
Assistant: Prepáčte, ale som špecializovaný na investičné poradenstvo. Na otázky o varení neviem odpovedať.
```

### Vylepšenia implementované po testovaní

1. **Validácia vstupov**
   - Kontrola záporných hodnôt
   - Kontrola percentuálnych hodnôt
   - Kontrola investičného horizontu
   - Kontrola súčtu percent

2. **Spracovanie chýb**
   - Jasné chybové hlásenia
   - Návody na opravu
   - Alternatívne návrhy

3. **Extrémne scenáre**
   - Minimálny investičný horizont (1 mesiac)
   - Maximálny investičný horizont (100 rokov)
   - Upozornenia na obmedzenia výpočtov

4. **Neočakávané požiadavky**
   - Zdvorilé odmietnutie nesúvisiacich otázok
   - Vysvetlenie obmedzení
   - Návody na alternatívne zdroje

## 3. Zhrnutie vylepšení

1. **Rozšírená funkcionalita**
   - Pridaná analýza rizika portfólia
   - Porovnanie rôznych investičných možností
   - Výpočty zloženého úroku
   - Odporúčania pre alokáciu aktív
   - Validácia vstupov
   - Spracovanie extrémnych scenárov

2. **Vylepšené odpovede**
   - Detailnejšie vysvetlenia
   - Kontextové odporúčania
   - Vyvážené investičné rady
   - Zrozumiteľné príklady
   - Jasné chybové hlásenia

3. **Nové nástroje**
   - Kalkulácia rizika portfólia
   - Porovnávanie investičných možností
   - Výpočty zloženého úroku
   - Validácia vstupov

4. **Lepšie promptovanie**
   - Kontextové otázky
   - Detailnejšie vysvetlenia
   - Praktické príklady
   - Zohľadnenie rizikových preferencií
   - Spracovanie chýb a extrémnych scenárov

## 4. Ukážky kódu

### Nové nástroje
```python
tools = [
    calculate_compound_interest,
    calculate_portfolio_risk,
    compare_investment_options
]
```

### Vylepšený systémový prompt
```python
sys_msg = SystemMessage(content="""You are an investment advisor assistant...""")
```