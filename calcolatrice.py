import os
import math
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich import box

# Inizializzazione della console di Rich
console = Console()

# Impostazioni predefinite per la calcolatrice
settings = {"precision": 2}  # Precisione dei risultati (numero di decimali)

def pulisci_terminale():
    """Funzione per pulire il terminale."""
    os.system("cls" if os.name == "nt" else "clear")

def calcola_espresso(espresso):
    """
    Funzione per calcolare l'espressione matematica data dall'utente.
    Sostituisce alcune funzioni matematiche e gestisce errori.
    """
    try:
        # Gestione speciale del logaritmo (base 10 predefinita)
        if "log(" in espresso and "," not in espresso:
            espresso = espresso.replace("log(", "math.log(") + ", 10)"
        else:
            # Sostituzione delle funzioni matematiche standard
            espresso = espresso.replace("sqrt", "math.sqrt").replace("^", "**")
            espresso = espresso.replace("sin", "math.sin(math.radians").replace("cos", "math.cos(math.radians").replace("tan", "math.tan(math.radians")
            espresso = espresso.replace("log", "math.log").replace("exp", "math.exp").replace("abs", "math.fabs")

        # Calcolo dell'espressione usando eval
        risultato = eval(espresso, {"__builtins__": None}, math.__dict__)
        return round(risultato, settings["precision"])
    except Exception as e:
        raise ValueError(f"Errore nell'elaborazione dell'espressione: {str(e)}")

def mostra_benvenuto():
    """Funzione per visualizzare il messaggio di benvenuto."""
    console.print(Panel.fit("[bold blue]Benvenuti nella Calcolatrice Semplice[/bold blue]", 
                            title="Calcolatrice", title_align="center", border_style="bold cyan", box=box.ROUNDED))

def mostra_menu():
    """Funzione per visualizzare il menu principale."""
    menu_text = """
    [bold cyan]Menu[/bold cyan]

    - [bold yellow]manual[/bold yellow]: Visualizza il manuale utente
    - [bold yellow]settings[/bold yellow]: Impostazioni
    - [bold yellow]exit[/bold yellow]: Esci dal programma
    """
    console.print(Panel.fit(menu_text, border_style="bold magenta", title="Menu", title_align="left", box=box.ROUNDED))

def mostra_risultato(espresso, risultato):
    """Funzione per visualizzare il risultato dell'espressione calcolata."""
    console.print(Panel.fit(f"Risultato: {espresso} = {risultato}", border_style="bold green", box=box.ROUNDED))

def mostra_errore(errore):
    """Funzione per visualizzare un messaggio di errore."""
    console.print(Panel.fit(f"Errore: {errore}", border_style="bold red", box=box.ROUNDED))

def mostra_manual():
    """Funzione per visualizzare il manuale utente."""
    pulisci_terminale()
    manual_md = """
# Manuale Utente

## Operazioni Supportate
- **Addizione**: `5 + 3`
- **Sottrazione**: `10 - 2`
- **Moltiplicazione**: `4 * 2`
- **Divisione**: `8 / 2`
- **Potenza**: `2 ^ 3`
- **Radice Quadrata**: `sqrt(16)`
- **Funzioni Trigonometriche**: `sin(45)`, `cos(30)`, `tan(60)`
- **Logaritmo**: `log(10)` per log base 10, `log(100, 10)` per specificare la base
- **Esponenziale**: `exp(2)`

## Comandi Aggiuntivi
- **Visualizza il manuale**: `manual`
- **Visualizza le impostazioni**: `settings`
- **Esci dal programma**: `exit`
"""
    console.print(Panel.fit(Markdown(manual_md), border_style="bold blue", title="Manuale", title_align="left", box=box.ROUNDED))
    Prompt.ask("\nPremi [bold cyan]Invio[/bold cyan] per tornare al menu...")

def mostra_settings():
    """Funzione per visualizzare e modificare le impostazioni."""
    pulisci_terminale()
    settings_md = f"""
# Impostazioni

- **Precisione dei Risultati**: {settings['precision']} decimali

## Cambiare Precisione
- Per cambiare la precisione, inserisci `precisione <numero>`, ad esempio `precisione 4` per 4 decimali.
"""
    console.print(Panel.fit(Markdown(settings_md), border_style="bold cyan", title="Impostazioni", title_align="left", box=box.ROUNDED))
    Prompt.ask("\nPremi [bold cyan]Invio[/bold cyan] per tornare al menu...")

def calcolatrice():
    """Funzione principale della calcolatrice."""
    pulisci_terminale()
    mostra_benvenuto()

    while True:
        mostra_menu()
        espresso = Prompt.ask("\nInserisci il comando o l'espressione matematica", console=console)

        if espresso.lower() == 'exit':
            break
        elif espresso.lower() == 'manual':
            mostra_manual()
            pulisci_terminale()
            continue
        elif espresso.lower() == 'settings':
            mostra_settings()
            pulisci_terminale()
            continue
        elif espresso.lower().startswith("precisione"):
            try:
                _, precisione = espresso.split()
                settings["precision"] = int(precisione)
                console.print(f"[bold green]Precisione impostata a {precisione} decimali[/bold green]")
            except:
                console.print("[bold red]Errore: Specifica un numero valido di decimali.[/bold red]")
            continue

        try:
            risultato = calcola_espresso(espresso)
            mostra_risultato(espresso, risultato)
        except ValueError as e:
            mostra_errore(str(e))

        Prompt.ask("\nPremi [bold cyan]Invio[/bold cyan] per continuare...")
        pulisci_terminale()

    pulisci_terminale()
    console.print(Panel.fit("[bold red]Grazie per aver utilizzato la Calcolatrice Semplice![/bold red]", 
                            title="Uscita", title_align="center", border_style="bold red", box=box.ROUNDED))

if __name__ == "__main__":
    calcolatrice()
