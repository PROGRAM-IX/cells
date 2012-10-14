import pygame
import datetime

def save_surface(surf):
    filename = ("ss" 
        + "_" + str(datetime.datetime.now().year) 
        + "-" + str(datetime.datetime.now().month)
        + "-" + str(datetime.datetime.now().day)
        + "_" + str(datetime.datetime.now().hour)
        + "-" + str(datetime.datetime.now().minute)
        + "-" + str(datetime.datetime.now().second)
        + ".png")
    save_surface_name(surf, filename)

def save_surface_name(surf, filename):
    pygame.image.save(surf, filename)
    print "Pretty sure that saved successfully to %s." % filename
