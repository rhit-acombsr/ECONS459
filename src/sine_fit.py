import numpy, scipy.optimize
import pylab as plt

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = numpy.array(tt)
    yy = numpy.array(yy)
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*numpy.pi)
    fitfunc = lambda t: A * numpy.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}

m = [-0.000397110, -0.000375824, -0.000242944, -0.000251010, -0.000144668, -0.000132188, -0.000204262, -0.000222111, -0.000236486, -0.000358479, -0.000319537, -0.000239561, -0.000229386, -0.000208126, -0.000281865, -0.000322537, -0.000366278, -0.000633120, -0.000566255, -0.000551444, -0.000597218, -0.000577550, -0.000563027, -0.000545276, -0.000533486, -0.000473743, -0.000490884, -0.000636521, -0.000830211, -0.000825113, -0.000802615, -0.000612158, -0.000507777, -0.000304033, -0.000171946, -0.000224754, -0.000277336, -0.000128656, -0.000201548, -0.000101917, 0.000056880, 0.000050843, 0.000110400, 0.000070523, 0.000106055, 0.000141539, 0.000175421, 0.000209725, 0.000066180, 0.000113327, -0.000000262, -0.000127645, -0.000008213, 0.000079815, -0.000012438, -0.000105053, -0.000078859, -0.000355034, -0.000569140, -0.000612818, -0.000589000, -0.000521657, -0.000354669, -0.000258921, -0.000214998, -0.000281614, -0.000195833, -0.000072304, 0.000004246, 0.000043566, 0.000122415, 0.000246751, 0.000124116, 0.000178921, 0.000255645, 0.000348565, 0.000297820, 0.000260610, 0.000363883, 0.000130174, -0.000107304, 0.000149364, 0.000240229, 0.000250944, 0.000198646, 0.000221703, -0.000093470, -0.000398468, -0.000397772, -0.000448075, -0.000600872, -0.000218065, 0.000208562, 0.000030125, 0.000138671]
# k = []
# for j in range(95):
#     k.append(j+1)
k= numpy.linspace(1,96,95)

res = fit_sin(k, m)
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )

plt.plot(k, m, "-k", label="y", linewidth=2)
# plt.plot(k, yynoise, "ok", label="y with noise")
plt.plot(k, res["fitfunc"](k), "r-", label="y fit curve", linewidth=2)
plt.legend(loc="best")
plt.show()

# Amplitude=0.00025986610059086976, Angular freq.=0.17687321969050923, phase=-0.04226280162448594, offset=-0.00020139674150492106, Max. Cov.=0.07398876598562121