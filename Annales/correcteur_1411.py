#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

import sys
import inspect
import traceback

def print_exception(msg, up=1):
    ex_type, ex, tb = sys.exc_info() # Exception type, exception, traceback
    print '== ' + msg + ':'
    if ex_type is AssertionError:
        print '  ' + str(ex)
    elif ex_type is NotImplementedError:
        print '  ' + str(ex)
    else:
        #traceback.print_tb(tb)  # Affichage du contexte
        print ' '.join(traceback.format_list(traceback.extract_tb(tb)[-up:])),
        print '  ** {}: {}'.format(ex_type, ex)

# fonction utile pour tester l'égalité sur les réels
def assert_floats(a, b, tol):
    try:
        test = abs(a-b) < abs(tol)
    except Exception:
        raise AssertionError("Test invalide")
    if not test:
        f = sys._getframe()                          # Stack courant
        while f.f_code.co_name.startswith("assert"): # Remonte le stack
            f = f.f_back
        raise AssertionError("Echec du test {} == {} (l.{})".format(
            a, b, f.f_lineno))


def assert_vectors(v, w, tol):
    assert_floats(v.x, w.x, tol)
    assert_floats(v.y, w.y, tol)

# fonctions de test de Vector
def test_Vector_init_2():
    tol = 1.e-6
    try:
        assert_floats(code.Vector().x, 0, tol)
        assert_floats(code.Vector(2, -8).y, -8, tol)
    except Exception as err:
        print_exception("Vector.__init__: assignation des variables")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Vector_init_3():
    tol = 1.e-6
    try:
        code.Vector("test")
    except (TypeError, ValueError):
        pass
    except Exception as err:
        print_exception("Vector.__init__: ne lève pas TypeError/ValueError")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Vector_str_2():
    try:
        assert(str(code.Vector(1,-2.653)) == "(1.00, -2.65)")
        assert(str(code.Vector(0,0)) == "(0.00, 0.00)")
        assert(str(code.Vector(10,-265.3)) == "(10.00, -265.30)")
    except Exception as err:
        print_exception("Vector.__str__")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Vector_add_2():
    tol = 1.e-6
    try:
        v0 = code.Vector()
        v1 = code.Vector(1, 1)
        v2 = code.Vector(1, -1)
        v3 = code.Vector(2, 0)
        v4 = code.Vector(3, -1)
        assert_vectors(v0+v0, v0, tol)
        assert_vectors(v0+v1, v1, tol)
        assert_vectors(v1+v2, v3, tol)
        assert_vectors(v2+v3, v4, tol)
    except Exception as err:
        print_exception("Vector.__add__")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Vector_mul_2():
    tol = 1.e-6
    try:
        v0 = code.Vector()
        v1 = code.Vector(1, 1)
        v2 = code.Vector(4, -9)
        v3 = v1*-16             # p*vecteur n'est pas supporté
        v4 = v2*3
        assert_floats(1*v0.x, 0, tol)
        assert_floats(1*v0.y, 0, tol)
        assert_floats(0*v1.x, 0, tol)
        assert_floats(0*v1.y, 0, tol)
        assert_floats(v3.y, -16, tol)
        assert_floats(v4.x, 12, tol)
        assert_floats(v4.y, -27, tol)
    except Exception as err:
        print_exception("Vector.__mul__")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Vector_scal_2():
    tol = 1.e-6
    try:
        v1 = code.Vector(1, 0)
        v2 = code.Vector(0, -10)
        v3 = code.Vector(3, 3)
        v4 = code.Vector(3, -3)
        v5 = code.Vector(3, -6)
        assert_floats(v1.scal(v2), 0, tol)
        assert_floats(v2.scal(v5), 60, tol)
        assert_floats(v3.scal(v4), 0, tol)
        assert_floats(v3.scal(v5), -9, tol)
        assert_floats(v4.scal(v5), 27, tol)
        assert_floats(v2.scal(v1), 0, tol)
        assert_floats(v5.scal(v2), 60, tol)
        assert_floats(v4.scal(v3), 0, tol)
        assert_floats(v5.scal(v3), -9, tol)
        assert_floats(v5.scal(v4), 27, tol)
    except Exception as err:
        print_exception("Vector.scal")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Vector_norm_2():
    tol = 1.e-6
    try:
        v0 = code.Vector()
        v1 = code.Vector(1, 1)
        v2 = code.Vector(4, -9)
        assert_floats(v0.norm(), 0, tol)
        assert_floats(v1.norm(), 2**0.5, tol)
        assert_floats(v2.norm(), 97**0.5, tol)
    except Exception as err:
        print_exception("Vector.norm")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

# fonctions de test de Simulation
def test_Simulation_init_2():
    tol = 1.e-6
    try:
        s = code.Simulation(5, 0.9, code.Vector(2, 1), 0.1)
        assert_floats(s.m, 5, tol)
        assert_floats(s.k, 0.9, tol)
        assert_vectors(s.r[0], code.Vector(), tol)
        assert_vectors(s.v[0], code.Vector(2, 1), tol)
    except Exception as err:
        print_exception("Simulation.__init__: affectation des variables")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Simulation_init_3():
    ok = [] ; raised = False
    try:
        code.Simulation("test", 0.5, code.Vector(1, 1), 1)
    except (TypeError, ValueError):
        ok += [True] ; raised = True
    except Exception as err:
        ok += [False] ; raised = True
        print_exception("test_Simulation_init_3 1")
    if not raised:
        ok += [False]
    raised = False
    try:
        code.Simulation(1, code.Vector(), code.Vector(1, 1), 1)
    except (TypeError, ValueError):
        ok += [True] ; raised = True
    except Exception as err:
        ok += [False] ; raised = True
        print_exception("test_Simulation_init_3 2")
    if not raised:      ok += [False]
    raised = False
    try:
        code.Simulation(1, 0.5, 3, 1)
    except (TypeError, ValueError):
        ok += [True] ; raised = True
    except Exception as err:
        ok += [False] ; raised = True
        print_exception("test_Simulation_init_3 3")
    if not raised:      ok += [False]
    raised = False
    try:
        code.Simulation(1, 0.5, code.Vector(1, 1), "test")
    except (TypeError, ValueError):
        ok += [True] ; raised = True
    except Exception as err:
        ok += [False] ; raised = True
        print_exception("test_Simulation_init_3 4")
    if not raised:      ok += [False]
    if False in ok:
        return False
    else:
        print "++", sys._getframe().f_code.co_name, "all OK"
        return True

def test_Simulation_init_4():
    raised = False
    ok = []
    try:
        code.Simulation(-3, 0.5, code.Vector(1, 1), 1)
    except (TypeError, ValueError):
        ok += [True] ; raised = True
    except Exception as err:
        ok += [False] ; raised = True
        print_exception("test_Simulation_init_4 1")
    if not raised: ok += [False]
    raised = False
    try:
        code.Simulation(1, 2, code.Vector(1, 1), 1)
    except (TypeError, ValueError):
        ok += [True] ; raised = True
    except Exception as err:
        ok += [False] ; raised = True
        print_exception("test_Simulation_init_4 2")
    if not raised: ok += [False]
    raised = False
    try:
        code.Simulation(1, 0.5, code.Vector(-1, -1), 1)
    except (TypeError, ValueError):
        ok += [True] ; raised = True
    except Exception as err:
        ok += [False] ; raised = True
        print_exception("test_Simulation_init_4 3")
    if not raised: ok += [False]
    raised = False
    try:
        code.Simulation(1, 0.5, code.Vector(1, 1), -6)
    except (TypeError, ValueError):
        ok += [True] ; raised = True
    except Exception as err:
        ok += [False] ; raised = True
        print_exception("test_Simulation_init_4 4")
    if not raised: ok += [False]
    if False in ok:
        return False
    print "++", sys._getframe().f_code.co_name, "all OK"
    return True

def test_Simulation_step_2():
    try:
        tol = 1.e-6
        s = code.Simulation(1, 0.01, code.Vector(1, 10), 1.)
        s.step()
        expV = code.Vector(1-0.01*101**0.5, 10-0.1*101**0.5-9.8)
        assert_vectors(s.r[-1], code.Vector(1, 10), tol)
        assert_vectors(s.v[-1], expV, tol)
        s = code.Simulation(2, 0.1, code.Vector(3, 4), 0.01)
        s.step()
        expV = code.Vector(2.9925, 3.892)
        assert_vectors(s.r[-1], code.Vector(0.03, 0.04), tol)
        assert_vectors(s.v[-1], expV, tol)
        s.step()
        expR = code.Vector(0.059925, 0.07892)
        expV = code.Vector(2.98515423, 3.78444620)
        assert_vectors(s.r[-1], expR, tol)
        assert_vectors(s.v[-1], expV, tol)
    except Exception as err:
        print_exception("Simulation.step")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Simulation_run_2():
    try:
        tol = 1.e-3
        # chute libre - conservation vx, xmax, indépendant de m
        s = code.Simulation(1, 0, code.Vector(0.1, 1), 1.e-4)
        s.run()
        assert_floats(s.r[-1].x, 0.2/9.8, tol)
        assert_floats(s.v[-1].x, 0.1, tol)
        s = code.Simulation(5, 0, code.Vector(0.1, 1), 1.e-4)
        s.run()
        assert_floats(s.r[-1].x, 0.2/9.8, tol)
        # frottements -> vitesse limite si démarrage suffisant
        s = code.Simulation(1./9.8, 0.01, code.Vector(1, 1000), 1.e-4)
        s.run()
        assert_vectors(s.v[-1], code.Vector(0., -10.), tol)
        s = code.Simulation(4/9.8, 0.01, code.Vector(1, 3000), 1.e-4)
        s.run()
        assert_vectors(s.v[-1], code.Vector(0., -20.), tol)
    except Exception as err:
        print_exception("Simulation.run")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Simulation_maxDistance_2():
    try:
        tol = 1.e-2
        s = code.Simulation(1, 0, code.Vector(1, 1), 1.e-4)
        s.run()
        assert_floats(s.maxDistance(), 2./9.8, tol)
        s = code.Simulation(6, 0, code.Vector(1, 1), 1.e-4)
        s.run()
        assert_floats(s.maxDistance(), 2./9.8, tol)
        s = code.Simulation(4, 0.01, code.Vector(1., 1.), 1.e-4)
        s.run()
        assert_floats(s.maxDistance(), 0.206, tol)
    except Exception as err:
        print_exception("Simulation.maxDistance")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Simulation_maxAltitude_2():
    try:
        tol = 1.e-2
        s = code.Simulation(1, 0, code.Vector(1, 1), 1.e-4)
        s.run()
        assert_floats(s.maxAltitude(), 0.5/9.8, tol)
        s = code.Simulation(6, 0, code.Vector(1, 1), 1.e-4)
        s.run()
        assert_floats(s.maxAltitude(), 0.5/9.8, tol)
        s = code.Simulation(4, 0.01, code.Vector(1., 1.), 1.e-4)
        s.run()
        assert_floats(s.maxAltitude(), 0.0515, tol)
    except Exception as err:
        print_exception("Simulation.maxAltitude")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Simulation_finalSpeed_2():
    try:
        tol = 1.e-2
        s = code.Simulation(1, 0, code.Vector(1, 1), 1.e-4)
        s.run()
        assert_vectors(s.finalSpeed(), code.Vector(1, -1), tol)
        s = code.Simulation(6, 0, code.Vector(1, 1), 1.e-4)
        s.run()
        assert_vectors(s.finalSpeed(), code.Vector(1, -1), tol)
        s = code.Simulation(4/9.8, 0.01, code.Vector(1, 3000), 1.e-4)
        s.run()
        assert_vectors(s.finalSpeed(), code.Vector(0, -20), tol)
    except Exception as err:
        print_exception("Simulation.finalSpeed")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True

def test_Simulation_energy_2():
    try:
        tol = 1.e-2
        s = code.Simulation(1, 0, code.Vector(1, 1), 1.e-4)
        s.run()
        assert_floats(s.energy()[0], 1, tol)
        assert_floats(s.energy()[-1], 1, tol)
        assert_floats(s.energy()[int(len(s.r)/2)], 1, tol)
        s = code.Simulation(6, 0, code.Vector(1, 1), 1.e-4)
        s.run()
        assert_floats(s.energy()[0], 6, tol)
        assert_floats(s.energy()[-1], 6, tol)
        assert_floats(s.energy()[int(len(s.r)/2)], 6, tol)
        # energie à la vitesse limite
        s = code.Simulation(1/9.8, 0.01, code.Vector(1, 3000), 1.e-4)
        s.run()
        assert_floats(s.energy()[0], 0.5/9.8*(3000**2+1), tol)
        assert_floats(s.energy()[-1], 50/9.8, tol)
    except Exception as err:
        print_exception("Simulation.energy")
        return False
    print "++", sys._getframe().f_code.co_name, "OK"
    return True


# fonction principale
if __name__ == '__main__':

    codename = sys.argv[1]
    if codename.endswith(".py"):
        codename = codename[:-3]

    # test à l'importation
    try:
        code = __import__(codename)
    except Exception as err:
        print_exception("Erreur à l'import")
        raise

    # Correction officielle
    correction = __import__("corrige_1411")

    note = 0

    # test de Vector : 7 points
    if test_Vector_init_2():  note += 1
    if test_Vector_init_3():  note += 1
    code.Vector.__init__ = correction.Vector.__init__.__func__
    if test_Vector_str_2():   note += 1
    code.Vector.__str__ = correction.Vector.__str__.__func__
    if test_Vector_add_2():   note += 1
    code.Vector.__add__ = correction.Vector.__add__.__func__
    if test_Vector_mul_2():   note += 1
    code.Vector.__mul__ = correction.Vector.__mul__.__func__
    if test_Vector_scal_2():  note += 1
    code.Vector.scal = correction.Vector.scal.__func__
    if test_Vector_norm_2():  note += 1
    code.Vector.norm = correction.Vector.norm.__func__

    # test de Simulation : 9 points
    if test_Simulation_init_2():  note += 1
    if test_Simulation_init_3():  note += 1
    if test_Simulation_init_4():  note += 1
    code.Simulation.__init__ = correction.Simulation.__init__.__func__
    if test_Simulation_step_2():  note += 1
    code.Simulation.step = correction.Simulation.step.__func__
    if test_Simulation_run_2():   note += 1
    code.Simulation.run = correction.Simulation.run.__func__
    if test_Simulation_maxDistance_2(): note += 1
    if test_Simulation_maxAltitude_2(): note += 1
    if test_Simulation_finalSpeed_2():  note += 1
    if test_Simulation_energy_2():  note += 1

    print "Note finale :", note, "/ 16"
