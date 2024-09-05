from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ScriptUploadForm
from .models import Script, Character, Scene, Element, Budget
from .utils import script_parser, character_analyzer, scene_breakdown, element_extractor, budget_estimator

@login_required
def upload_script(request):
    if request.method == 'POST':
        form = ScriptUploadForm(request.POST)
        if form.is_valid():
            script = form.save(commit=False)
            script.user = request.user
            script.save()
            return redirect('analyze_script', script_id=script.id)
    else:
        form = ScriptUploadForm()
    return render(request, 'scripdown_python/upload_script.html', {'form': form})

@login_required
def analyze_script(request, script_id):
    script = Script.objects.get(id=script_id)
    
    try:
        # Parse the script
        parsed_script = script_parser.parse(script.content)
        
        # Analyze characters
        characters = character_analyzer.analyze(parsed_script)
        for char in characters:
            Character.objects.create(script=script, name=char['name'], importance=char['importance'])
    
        # Break down scenes
        scenes = scene_breakdown.breakdown(parsed_script)
        for scene in scenes:
            Scene.objects.create(script=script, number=scene['number'], location=scene['location'], description=scene['description'])
    
        # Extract elements
        elements = element_extractor.extract(parsed_script)
        for element in elements:
            Element.objects.create(script=script, category=element['category'], description=element['description'])
    
        # Estimate budget
        budget_data = budget_estimator.estimate(script, characters, scenes, elements)
        budget = Budget.objects.create(
           script=script,
           total_estimate=budget_data['total_estimate'],
           breakdown=budget_data['breakdown']
        )

        messages.success(request, "Script analysis completed successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred during script analysis: {str(e)}")
        return redirect('upload_script')
    
    return render(request, 'scripdown_python/analysis_result.html', {
        'script': script,
        'characters': characters,
        'scenes': scenes,
        'elements': elements,
        'budget': budget,
    })

@login_required
def adjust_budget(request, script_id):
    script = Script.objects.get(id=script_id)
    budget = script.budget
    
    if request.method == 'POST':
        # Handle budget adjustments
        adjustment_percentage = float(request.POST.get('adjustment', 0))
        updated_budget = budget_estimator.recalculate(budget, adjustment_percentage)
        budget.total_estimate = updated_budget['total_estimate']
        budget.breakdown = updated_budget['breakdown']
        budget.save()
    
    return render(request, 'scripdown_python/budget_estimate.html', {'budget': budget})