"""The 27 standards retrieved and verified from the CASE Network, plus the panel."""

from build import esc

STD = {
    "MP1": "Make sense of problems and persevere in solving them.",
    "MP2": "Reason abstractly and quantitatively.",
    "MP3": "Construct viable arguments and critique the reasoning of others.",
    "MP4": "Model with mathematics.",
    "MP5": "Use appropriate tools strategically.",
    "MP6": "Attend to precision.",
    "MP7": "Look for and make use of structure.",
    "MP8": "Look for and express regularity in repeated reasoning.",
    "5.G.A.1": (
        "Use a pair of perpendicular number lines, called axes, to define a coordinate "
        "system, with the intersection of the lines (the origin) arranged to coincide "
        "with the 0 on each line and a given point in the plane located by using an "
        "ordered pair of numbers, called its coordinates."
    ),
    "6.EE.A.2": (
        "Write, read, and evaluate expressions in which letters stand for numbers."
    ),
    "6.EE.B.6": (
        "Use variables to represent numbers and write expressions when solving a "
        "real-world or mathematical problem; understand that a variable can represent "
        "an unknown number, or, depending on the purpose at hand, any number in a "
        "specified set."
    ),
    "6.NS.C.8": (
        "Solve real-world and mathematical problems by graphing points in all four "
        "quadrants of the coordinate plane. Include use of coordinates and absolute "
        "value to find distances between points with the same first coordinate or the "
        "same second coordinate."
    ),
    "6.RP.A.3": (
        "Use ratio and rate reasoning to solve real-world and mathematical problems, "
        "e.g., by reasoning about tables of equivalent ratios, tape diagrams, double "
        "number line diagrams, or equations."
    ),
    "6.SP.B.4": (
        "Display numerical data in plots on a number line, including dot plots, "
        "histograms, and box plots."
    ),
    "6.SP.B.5.a": (
        "Summarize numerical data sets in relation to their context, such as by "
        "reporting the number of observations."
    ),
    "6.SP.B.5.c": (
        "Summarize numerical data sets in relation to their context, such as by giving "
        "quantitative measures of center (median and/or mean) and variability "
        "(interquartile range and/or mean absolute deviation), as well as describing any "
        "overall pattern and any striking deviations from the overall pattern with "
        "reference to the context in which the data were gathered."
    ),
    "7.RP.A.2": "Recognize and represent proportional relationships between quantities.",
    "7.SP.A.1": (
        "Understand that statistics can be used to gain information about a population "
        "by examining a sample of the population; generalizations about a population "
        "from a sample are valid only if the sample is representative of that "
        "population. Understand that random sampling tends to produce representative "
        "samples and support valid inferences."
    ),
    "7.SP.C.5": (
        "Understand that the probability of a chance event is a number between 0 and 1 "
        "that expresses the likelihood of the event occurring. Larger numbers indicate "
        "greater likelihood. A probability near 0 indicates an unlikely event, a "
        "probability around 1/2 indicates an event that is neither unlikely nor likely, "
        "and a probability near 1 indicates a likely event."
    ),
    "7.SP.C.6": (
        "Approximate the probability of a chance event by collecting data on the chance "
        "process that produces it and observing its long-run relative frequency, and "
        "predict the approximate relative frequency given the probability."
    ),
    "7.SP.C.7": (
        "Develop a probability model and use it to find probabilities of events. "
        "Compare probabilities from a model to observed frequencies; if the agreement "
        "is not good, explain possible sources of the discrepancy."
    ),
    "7.SP.C.8": (
        "Find probabilities of compound events using organized lists, tables, tree "
        "diagrams, and simulation."
    ),
    "8.EE.A.1": (
        "Know and apply the properties of integer exponents to generate equivalent "
        "numerical expressions."
    ),
    "8.F.A.1": (
        "Understand that a function is a rule that assigns to each input exactly one "
        "output. The graph of a function is the set of ordered pairs consisting of an "
        "input and the corresponding output."
    ),
    "8.F.B.4": (
        "Construct a function to model a linear relationship between two quantities. "
        "Determine the rate of change and initial value of the function from a "
        "description of a relationship or from two (x, y) values, including reading "
        "these from a table or from a graph. Interpret the rate of change and initial "
        "value of a linear function in terms of the situation it models, and in terms "
        "of its graph or a table of values."
    ),
    "8.F.B.5": (
        "Describe qualitatively the functional relationship between two quantities by "
        "analyzing a graph (e.g., where the function is increasing or decreasing, "
        "linear or nonlinear). Sketch a graph that exhibits the qualitative features of "
        "a function that has been described verbally."
    ),
    "8.G.B.7": (
        "Apply the Pythagorean Theorem to determine unknown side lengths in right "
        "triangles in real-world and mathematical problems in two and three dimensions."
    ),
}

MAPNOTE = (
    '<p class="mapnote">Mapped to the Common Core State Standards for Mathematics '
    "(Multi-State). Each code and its wording was retrieved from the CASE Network "
    "through the Learning Commons Knowledge Graph on 12 September 2026. New York's own "
    "Computer Science and Digital Fluency framework and the CSTA standards are not "
    "carried in that graph, so no code from either appears anywhere on this site.</p>"
    '<p class="mapnote">Two deliberate deviations from the retrieved text. The "for '
    "example\u2026\" illustrations attached to 7.SP.C.6 and 8.EE.A.1 are omitted, since "
    "they illustrate rather than state the standard. And where the source carries "
    "markup, italics or mathematical notation, it is rendered as plain text: 7.SP.C.5's "
    "fraction appears here as 1/2, and the italic stem of 6.SP.B.5.a and 6.SP.B.5.c is "
    "plain. Nothing else was shortened. Codes 6.SP.B.5.a and 6.SP.B.5.c are the "
    "lettered children of 6.SP.B.5, whose own statement is only a stem ending in a "
    "colon; the children carry that stem and are quoted in full.</p>"
)


def panel(codes, timing, watch, retouch=None, extras=""):
    """Return the teacher panel. Three standards maximum."""
    assert len(codes) <= 3, f"more than three standards: {codes}"
    rows = ""
    for c in codes:
        rows += f'<p class="stdline"><span class="std">{esc(c)}</span> {esc(STD[c])}</p>\n'
    rt = f"<h3>Concept this session re-touches</h3><p>{retouch}</p>" if retouch else ""
    return (
        '<section class="panel"><h2>Teacher panel</h2>'
        f"{rt}<h3>Standards</h3>"
        f"{rows}"
        f"{MAPNOTE}<h3>Timing</h3>{timing}"
        f"<h3>What to watch for</h3>{watch}{extras}</section>\n"
    )
