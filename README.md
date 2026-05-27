# Relativistic Mission Simulator

A visual companion to *Project Hail Mary*.

Live: **https://mayankkishore.com/hail-mary/**

Demo: [`demo.mp4`](demo.mp4)
Writeup: [`writeup.pdf`](writeup.pdf)

https://github.com/KishoreMayank/hail-mary/assets/demo.mp4

<video src="demo.mp4" controls width="720"></video>

---

I chose **Theme 1: Exploration and Understanding.**

I'd just watched *Project Hail Mary* and wanted to better visualize time dilation to improve my understanding. Most explainers use the clock example. The unintuitive part is that two observers can't agree on what "now" means by the end of the trip.

So I built a visualization to see both ideas at once. A Minkowski spacetime diagram with each observer's line of simultaneity drawn on top.

> *Simultaneity: the set of events two observers consider "happening at the same time."*

## What's non-obvious

The way to teach relativity is to render the invisible thing:

1. **Spacetime diagram as the hero.** This is the diagram physicists actually reason in and it's useful to help readers visualize this as physicists do.
2. **Simultaneity drawn live.** "Now" is a tilted line in spacetime, and the tilt depends on who's asking. Render both observers' lines on the same diagram and the disagreement stops being a paradox. At *v ≈ 0* they overlap. At *v ≈ c* they fan apart.
3. **The flip as a visible discontinuity.** Then the ship turns around, its line of simultaneity snaps to the opposite slope. Earth's "now" leaps forward over years. That jump is the twin paradox resolution — the missing time the traveling twin owes Earth, visualized.

## Decisions and tradeoffs

1. **Spacetime diagram as hero, star map as anchor.** Star map keeps them oriented while the spacetime view does the teaching.
2. **Simultaneity as a moving line, not a number.** A "Δt = 4.2y" badge would be easier, but it wouldn't be instructive enough.
3. **Constant proper acceleration, not constant velocity.** γ has to actually vary across the trip, or the flip has nothing interesting to show.

## How I'd extend it

**A 3D Minkowski diagram.** I would like to drop the "line" simplification and render the entire light cone where we can plot the trip as a curve through it and allow the user to orbit.

**LLM tutor in the margin.** Answers *"why is the line tilted like that right now?"* against the live state. It would be great if it could interact with the diagram and make changes to it as the user requests — generative software that yields better learning outcomes.

## Time spent

~4 hours, split evenly across the physics layer, the spacetime diagram and simultaneity, the round-trip flip, and final polish.
