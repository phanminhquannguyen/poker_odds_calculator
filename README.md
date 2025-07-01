Poker Odds Calculator

Aim
The goal of this project is to build a poker odds calculator website that estimate the winning probability of a Texas Hold'em hand, given your cards, oppoenent hands, and any known community cards.

Methodology
Monte Carlo simulation is used to achieve an accurate result. The program runs a large number of randomized simulations by completing the unkonw community cards with randomly drawns one and evaluating each players's best 5-card hand using a evaluation function based on poker hand strength. By aggregating the results accorss many simulations, the program estimates win, tie and loss probabilities.

Why Monte Carlo Simulation?
Poker involves a vast number of possible card combination, especially when community card are completely  unknown. Monte Carlo simulations provides a practical way to approximate outcomes without enumerating every possible combination of hands. It leverages the Law of Large Numbers, which ensures that as the number of simulation increases, the estimated probability converge to their true value. This approach allows for flexibility, fast and reasonably accurate odds calculation in real time.

Website interface
<img width="382" alt="Screenshot 2025-07-01 at 9 07 38 pm" src="https://github.com/user-attachments/assets/ee5ec6df-5774-4baa-9cb6-201599b3090e" />
