from . import agent, board, stats
import matplotlib.pyplot as plt


def train(n_games):
    n_games = int(n_games)
    window = 10
    learning_rate = 0.3
    discount_factor = 0.9
    epsilon = 0.1

    b = board.Board()
    a = agent.QAgent(
        learning_rate=learning_rate, discount_factor=discount_factor, epsilon=epsilon
    )

    ties = stats.RA(window)
    im = stats.RA(window)

    ties_trace = []
    im_trace = []

    for _ in range(n_games):
        b.reset()

        current_state = b.get_state()
        while b._winner is None:
            move = a.get_move(current_state)

            reward = b.move(move)

            next_state = b.get_state()

            a.update(current_state, move, reward, next_state)
            current_state = next_state

            im.add(int(reward == -1))
            if im.is_ready():
                im_trace.append(float(im))

            if b._winner is not None:
                ties.add(int(b._winner == "tie"))
                if ties.is_ready():
                    ties_trace.append(float(ties))

    a.save_to_file()

    # Create subplots with 2 rows and 1 column
    fig, axs = plt.subplots(2, 1, figsize=(10, 12))

    # Plot the rolling average of ties
    axs[0].plot(ties_trace, label="Ties")
    axs[0].set_xlabel("Episodes")
    axs[0].set_ylabel("Rolling Average")
    axs[0].set_title("Rolling Average of Ties over Episodes")
    axs[0].legend()
    axs[0].grid(True)

    # Plot the rolling average of illegal moves
    axs[1].plot(im_trace, label="Illegal Moves")
    axs[1].set_xlabel("Episodes")
    axs[1].set_ylabel("Rolling Average")
    axs[1].set_title("Rolling Average of Illegal Moves over Episodes")
    axs[1].legend()
    axs[1].grid(True)

    # Adjust layout to prevent overlapping
    plt.tight_layout()

    # Show the plot
    plt.show()
