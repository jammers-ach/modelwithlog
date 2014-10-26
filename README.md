# jdjangoextensions

This is a set of extentions for django that Jammers find common


## model stamps

Django has a cool internal thing for logging changes made to objects when they
are created through the model admin, however it fails in certain places.

 * when you're not using the model admin
 * when you need to access them
 * When you have hirearchical models. E.g. someone changes a picture and you
   want the original blog post to have a notificaiton

Each instance of a model has a set of stamps. Each stamp has a colour (user)
and some information. Every time the model is changed it is stamped with the
type of change (Adition, Change, Deletion) and if it's been edited with a form
you can pass in the form for it to find a list of changed fields.

**there should be a picture here**


## usage

## Installing

Make sure jdjangoextensions is in your installed apps, and then make sure that
every extends `modelWithLog`

N.b. I haven't seen what happens as far as migrations go when you take an
existing model and then change it's base class to modelWithLog.

## 

## templates

It should be easy to see who has changed a model when and how

## safe deleting

When an object in the UI is deleted it's hard to tell if they are going to
destroy anything with cascades. `safedelete()` will only delete an object if
it's not going to delete any other objects due to cascades.

Obviously it's slower than a normal delete
