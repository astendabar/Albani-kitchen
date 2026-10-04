import json,re
d=json.load(open('recipes-source.json'))

CAT={
 'Loaded Hummus Bowl':'Main',
 'Shaved Brussels Sprout Salad with Chicken and Ginger Miso Dressing':'Main',
 'Shakshuka with Pickled Onions and Avocado':'Breakfast',
 'Kimchi Salad with Crispy Chickpeas':'Main',
 'Almond Chicken Tenders and Sauerkraut Slaw':'Main',
 'Garlic-Ginger Tempeh and Broccoli Over Quinoa':'Main',
 'Kimchi Stew with Tofu':'Soup',
 'Prosciutto, Spinach, and Asparagus Frittata':'Breakfast',
 'Brats with Sautéed Apples and Onions (Serve with Sauerkraut)':'Main',
 'Coconut and Kale Lentil Soup':'Soup',
 'Pulled Pork in Bone Broth':'Main',
 'Bacon-Avo-Egg (Bacon, Avocado, Egg)':'Breakfast',
 'Roasted Leg of Lamb':'Main',
 'The Best Roasted Chicken':'Main',
 'Ketobiotic Waffles':'Breakfast',
 'Crustless Everything Quiche':'Breakfast',
 'Breadcrumb-Free Crab Cakes':'Main',
 'Healthy Chicken Nuggets':'Main',
 'Purple Gold Kraut':'Condiment',
 'Yellow Cauliflower Tortillas':'Side',
 'Fresh Mint and Pea Spread':'Dip',
 'Meyer Lemon-Ginger Salmon':'Main',
 'Braised Beef Collagen Boost':'Main',
 'Salmon in Parchment Paper':'Main',
 'Yellowed Cauliflower':'Side',
 'Green Beans with Caramelized Shallots':'Side',
 'Cardamom Carrot Fries':'Side',
 'Spicy Zucchini Apple Muffins':'Snack',
 'Almond Coconut Bread':'Side',
 "Mindy's Magic Salad Dressing":'Dressing',
 'Kale Chips':'Snack',
 'Flaxseed-Crusted Salmon with a Roasted Squash and Broccoli Salad':'Main',
 'Pumpkin Chickpea Curry Stew':'Soup',
 'Sesame Ginger-Roasted Chicken and Sweet Potato with a Fennel and Pickled Beet Salad':'Main',
 'Chipotle Black Bean-Stuffed Sweet Potatoes with Cilantro-Lime Cabbage Slaw':'Main',
 'Shrimp Scampi and a Warm Bacon Balsamic Squash and Dandelion Salad':'Main',
 'Ghee-Basted Pork Chops, Sautéed Fennel, and Leeks with Kale and Roasted Potatoes':'Main',
 'Chickpea Pancakes with Sautéed Beans and Greens with a Lemon Tahini Dressing':'Main',
 'White Bean and Kale Soup':'Soup',
 'Herby Steaks with Mashed Potatoes and Roasted Veggie Medley':'Main',
 'Seed-Crusted Cauliflower Steaks with Arugula Chimichurri-Dressed Beans and Sweet Potato Fries':'Main',
 'Quinoa Tabouli':'Side',
 'Black and Orange Rice':'Side',
 'Sweet Potato Hash Browns':'Side',
 'Roasted Butternut Squash Soup':'Soup',
 'Cacao Quinoa Cake':'Dessert',
 'Avocado Blueberry Smoothie':'Beverage',
 'Chocolatey Chia Fat Bombs':'Dessert',
 'Avocado and Smoked Salmon with PPP "Everything Bagel" Seasoning':'Breakfast',
 'Fried Eggs with Kimchi':'Breakfast',
 'Mixed-Nut Coconut Fat Bombs':'Dessert',
 'Burger Patty with Guacamole':'Main',
 'Vanilla Bean Chia Pudding with Berries and Chocolate':'Dessert',
 'Tuna Salad-Stuffed Avocado':'Main',
 'Strawberry Mint Kefir Smoothie':'Beverage',
 'Garlicky Cider Spinach with Jammy Eggs':'Breakfast',
 'Spiced Coconut Curry Hummus':'Dip',
 'Coconut Cacao Chia Pudding':'Dessert',
 'Pumpkin Spice Spread':'Dip',
 'Basic Beef Bone Broth':'Condiment',
 'Steak Salad with Baked Tomatoes and Tarragon Dressing':'Main',
}
out=[]
for i,r in enumerate(d):
    desc=re.sub(r'\[span_\d+\]\((start|end)_span\)','',r['description']).strip()
    serv=re.search(r'\(([^)]*per serving[^)]*)\)',desc)
    veg='(V)' in r['name']
    name=r['name'].replace(' (V)','').strip()
    n=r['nutrition']
    g=lambda k:int(re.sub(r'\D','',n[k]) or 0)
    out.append(dict(id=i,name=name,cat=CAT.get(name,'Main'),veg=veg,yield_=r['recipeYield'],serving=serv.group(1) if serv else '',
      ing=r['recipeIngredient'],steps=[s['text'] for s in r['recipeInstructions']],
      f=g('fatContent'),c=g('carbohydrateContent'),p=g('proteinContent')))
fix={'Bacon-Avo-Egg (Bacon, Avocado, Egg)':dict(p=22),'Fresh Mint and Pea Spread':dict(f=7,c=4,p=2)}
C={'140':'60','145':'63','350':'180','375':'190','400':'200','425':'220'}
cv=lambda x:re.sub(r'(\d+)°F',lambda m:C[m.group(1)]+'°C',x)
for o in out:
    o['ing']=[cv(i) for i in o['ing']]
    o['steps']=[cv(t) for t in o['steps']]
for o in out:
    o['ing']=[i.replace('bulgur or quinoa','quinoa') for i in o['ing']]
    o['steps']=[t.replace('prepared bulgur','prepared quinoa') for t in o['steps']]
for o in out:
    o.update(fix.get(o['name'],{}))
GL=[
 (r'bulgur','Bulgur is wheat. Use the quinoa option.'),
 (r'miso','Some miso is made with barley. Choose a rice or soy miso labelled gluten-free.'),
 (r'\bbrats?\b','Some bratwurst contains wheat fillers or breadcrumbs. Choose one labelled gluten-free.'),
 (r'chili paste','Gochujang and many chili pastes contain wheat. Choose one labelled gluten-free.'),
 (r'curry paste','Some curry pastes contain wheat. Check the label.'),
 (r'kimchi','Some store-bought kimchi uses wheat-based sauces. Check the label or make your own.'),
 (r'tempeh','Some tempeh is made with barley or mixed grains. Choose plain soy tempeh.'),
 (r'(vegetable|chicken) broth|^[^(]*\bbone broth(?!.*page)','Store-bought broth can contain wheat. Check the label or use homemade broth.'),
]
for o in out:
    notes=[]
    for pat,msg in GL:
        if any(re.search(pat,i,re.I) for i in o['ing']) and msg not in notes: notes.append(msg)
    o['gl']=notes
out.append(dict(id=len(out),name='Steak Salad with Baked Tomatoes and Tarragon Dressing',veg=False,yield_='4 servings',serving='',
  src='https://www.valdemarsro.dk/steak-salat-med-bagte-tomater-og-estragondressing/',srcname='Valdemarsro',
  ing=['## Baked tomatoes','200 g cherry tomatoes, halved','200 g plum tomatoes, halved','Olive oil, salt and freshly ground black pepper',
       '## Tarragon dressing','1 handful fresh tarragon, finely chopped','1 teaspoon onion powder','1 tablespoon coarse-grain mustard','1 organic lemon, finely grated zest and a little juice','2 dl crème fraîche (18%)','2 tablespoons mayonnaise','Salt and freshly ground black pepper',
       '## Steak salad','600 g flank steak','1 head curly leaf lettuce','70 g arugula','1/2 cucumber, halved and sliced','1 red onion, cut into thin wedges','1 avocado, thinly sliced','1 tablespoon fresh tarragon, finely chopped, for sprinkling','20 g butter, for frying','Salt and freshly ground black pepper'],
  steps=['Baked tomatoes: Place the tomatoes cut side up on a baking tray. Drizzle with olive oil and sprinkle with salt and pepper. Bake in an oven preheated to 200°C (fan) for 25 minutes, then leave to cool until lukewarm on the tray.',
         'Tarragon dressing: Stir all the ingredients together except the lemon juice. Season to taste with salt, pepper and lemon juice, then let the dressing stand so the flavours develop.',
         'Steak: Heat a pan and add the butter. Season the meat with salt and pepper and fry for 2 to 3 minutes on each side. Let it rest for 5 minutes, then cut into slices.',
         'Serve: Arrange the lettuce and arugula with some of the dressing. Top with the baked tomatoes, cucumber, red onion and avocado. Add the sliced steak and sprinkle with salt, pepper and tarragon. Spoon over the rest of the dressing and serve straight away.'],
  cat='Main',f=37,c=12,p=35,gl=[]))
out.append(dict(id=len(out),name='Butter Chicken with Oat Rice',veg=False,yield_='4 servings',serving='',
  src='https://www.valsemollen.dk/opskrifter/butter-chicken-med-havreris/',srcname='Valsemøllen',
  ing=['400 g chicken breast or fillet','15 g fresh ginger, grated or finely chopped','4 cloves garlic, grated or finely chopped',
       '2 teaspoons ground coriander','2 teaspoons turmeric','2 tablespoons garam masala','1.5 dl Greek or Turkish yogurt',
       '2 tablespoons butter','2 onions','50 g butter','Salt and pepper','1/2-1 green chili, to taste (optional)',
       '2 cans chopped or crushed tomatoes','2.5 dl heavy cream','Oat rice, to serve (quantity as needed; cook according to package instructions, optionally with ginger or a cinnamon stick)'],
  steps=['Cut the chicken into cubes and place in a bowl with the ginger, garlic, dried spices and yogurt. Mix well and refrigerate for at least 40 minutes, longer if possible.',
         'Heat butter in a large frying pan and fry the marinated chicken pieces, about 2-3 minutes on each side. Remove the chicken from the pan.',
         'Cook the oat rice according to the package instructions.',
         'Peel and chop the onions. Heat the butter in the pan and sauté the onions over medium heat, stirring, until golden, about 5-6 minutes; this takes patience but adds real depth of flavor. Season with salt and pepper. Add the chopped chili and the tomatoes and let simmer for 5 minutes. Blend the mixture. Add the cream and the fried chicken, bring to a boil and let simmer a few minutes more. Season to taste with salt and, if needed, a little sugar.',
         'Serve with oat rice, optionally cooked with ginger or a cinnamon stick.'],
  cat='Main',f=45,c=18,p=37,
  gl=['Oats are often cross-contaminated with wheat during growing or processing. Choose rolled oats or oat rice labelled gluten-free if this matters to you.']))
data=json.dumps(out,ensure_ascii=False).replace('</','<\\/')
html=open('template.html').read().replace('/*DATA*/[]',data)
open('ketobiotic-recipes.html','w').write(html)
print(len(out))
