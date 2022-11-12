from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.registrant import Registrant
from flask_app.models.recipe import Recipe
from flask import flash


@app.route("/recipes/dashboard")
def recipes_dashboard():
    if "registrant_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")
    data = {
        "id": session['registrant_id']
    }
    registrant = Registrant.get_by_id(data)
    recipes = Recipe.get_all()

    return render_template("dashboard.html", registrant=registrant, recipes=recipes)

@app.route("/recipes/<int:recipe_id>")
def recipe_info(recipe_id):
    
    registrant_data = {
        "id" : session['registrant_id']
    }
    registrant = Registrant.get_by_id(registrant_data)
    
    # recipe_data = {
    #     "id" :['recipe_id']
    # }
    recipe = Recipe.get_by_id(recipe_id)
    
    return render_template("recipe_info.html", registrant=registrant, recipe=recipe)

@app.route("/recipes/create")
def recipe_create_page():
    return render_template("create.html")

@app.route("/recipes/edit/<int:recipe_id>")
def recipe_edit_page(recipe_id):
    session['recipe_id'] = recipe_id
    recipe = Recipe.get_by_id(recipe_id)
    return render_template("edit.html", recipe=recipe)

######## POST and ACTION METHODS ########

@app.route("/recipes", methods=["POST"])
def create_recipe():
    if Recipe.is_valid(request.form):
        Recipe.create_valid_recipe(request.form)
    return redirect('/recipes/dashboard')

@app.route("/recipes/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    print(request.form,'*'*60)
    print(session['registrant_id'])
    valid_recipe = Recipe.update_recipe(request.form, session["registrant_id"])

    if not valid_recipe:
        return redirect(f"/recipes/edit/{recipe_id}")
        
    return redirect(f"/recipes/{recipe_id}")

@app.route("/recipes/delete/<int:recipe_id>")
def delete_by_id(recipe_id):
    Recipe.delete_recipe_by_id(recipe_id)
    return redirect("/recipes/dashboard")