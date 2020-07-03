<template>
    <section class="container my-3">
        <h1>About Meals Count Algorithms</h1?
        <p>(AKA "Strategies")</p>

        <p>
            Meals Count uses several different algorithms (we call them "strategies") to try to optimize a district's reimbursement. Here are simplified descriptions for the curious of how each algorithm works. When you submit a district to be optimized, Meals Count will run all algorithms in their default configuration, and show you the recommended grouping from the algorithm that has the highest reimbursement. Each algorithm has a link to its corresponding file in the Meals Count source code (which is Open Source and available to all).
        </p>

        <h2>Exhaustive</h2>
        <a href="https://github.com/opensandiego/mealscount-backend/blob/validate/strategies/exhaustive.py" target="_blank">(source)</a>
        <p>The Exhaustive algorithm runs every possible configuration of schools in the submitted district. From what we have seen, this practically stops being possible at around 11 schools. It might be possible to go to 12 or 13 if you want to spend money on compute power. Any district that gets an "Exhaustive" result can be assured that this is the maximum possible reimbursement!</p>

        <h2>NYCMODA</h2>
        <a href="https://github.com/opensandiego/mealscount-backend/blob/validate/strategies/nyc_moda_simulated_annealing.py" target="_blank">(source)</a>
        <p>The current best performing algorithm for districts over 11 schools is a "Stochastic Climb with Simulated Annealing" algorithm originally developed for/by the New York City Mayor's Office of Data Analytics, with the project name <a href="https://moda-nyc.github.io/Project-Library/projects/free_lunch_for_all/" target="_blank">Free Lunch for All</a>. It has been ported over to Meals Count and optimized. This is similar to a "genetic algorithm" in that it starts with a random grouping, then each step it moves a school from one group to another. If the result increases revenue, the change is kept. If not, it is discarded. These random school move iterations are done a bunch of times (e.g. 1000 iterations), for a bunch of different starting random groupings. The end result is chosen as the one that maximizes reimbursement. By default MealsCount does this a limited number of times (which already outperforms all other algorithms), but districts interested in increasing the iteration to maximize potential can either contact the Meals Count team, or try out the code themselves.</p>

        <h2>"One Group" and "One To One"</h2>
        <a href="" target="_blank">(source)</a>
        <p>The One Group and One To One are simply as described. One group puts all schools in a group, One To One puts each school in its own group. There really isn't any magic here, but it is a good point for comparison, and surprisingly does end up being the best strategy.</p>

        <h2>Pairs</h2>
        <a href="https://github.com/opensandiego/mealscount-backend/blob/validate/strategies/pairs.py" target="_blank">(source)</a>
        <p>Pairs is a heuristic, or rules based algorithm that walks through the high ISP schools above the 62.5% threshold, and pairs each one with a school below the threshold, to raise them together (provided the resulting group exceeds the threshold). This is generally the most successful "heuristic" algorithm for districts over the "Exhaustive" 11 school threshold.
            </p>

        <h2>Spread</h2>
        <a href="https://github.com/opensandiego/mealscount-backend/blob/validate/strategies/spread.py" target="_blank">(source)</a>
        <p>Similar to Pairs, spread walks through the top ISP schools, but instead of just pairing, it packs as many schools into each group until that group just hovers above the threshold. This sounds great but isn't quite as good as Pairs in practice.</p>

        <h2>Binning</h2>
        <a href="https://github.com/opensandiego/mealscount-backend/blob/validate/strategies/binning.py" target="_blank">(source)</a>
        <p>Binning follows a naive approach to group the highest ISPs together, then group in chunks lower ISP schools until we hit the bottom threshold. This is rarely a winning strategy, as amount over 62.5% in ISP is "wasted" unless paired with a lower ISP school. This was the first algorithms to be created for Meals Count.</p>

        <h2>Improving on This</h2> 
        <div class="alert alert-info">
            <p>If you think you have an idea for how to improve on this, please don't hesitate to fork the repository or <router-link to="contact/">contact us</router-link>!</p>
            <p>Meals Count does most of the work in managing the school data, so to test a strategy you can just extend and implement a new "CEPStrategy" class. There is a <a href="https://github.com/opensandiego/mealscount-backend/blob/validate/CEP%20Estimator.ipynb" target="_blank">jupyter notebook</a> available for data scientists that provides examples in using the Meals Count tools.</p>
        </div>

    </section>
</template>

<style scoped>
    h2 { 
        margin-top: 30px;

    }
</style>