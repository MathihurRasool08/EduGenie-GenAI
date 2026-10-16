const task = document.getElementById('task');
const input = document.getElementById('inputText');
const button = document.getElementById('submitBtn');
const result = document.getElementById('result');
const status = document.getElementById('status');

const endpoints = {
  qa: '/qa', explain: '/explain', quiz: '/quiz', summarize: '/summarize', learn: '/learn/recommendations'
};

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}
function renderText(text) {
  return `<div class="text-output">${escapeHtml(text).replace(/\n/g, '<br>')}</div>`;
}
function renderQuiz(data) {
  return `<h2>${escapeHtml(data.title)}</h2>${data.questions.map((q, i) => `
    <article class="quiz-question"><h3>${i + 1}. ${escapeHtml(q.question)}</h3>
      <div class="options">${q.options.map(o => `<button class="option" data-answer="${escapeHtml(q.correct_answer)}" data-value="${escapeHtml(o)}">${escapeHtml(o)}</button>`).join('')}</div>
      <p class="feedback" hidden></p>
    </article>`).join('')}`;
}
function renderLearning(data) {
  return `<h2>${escapeHtml(data.topic)} — Learning Path</h2><p><strong>Level:</strong> ${escapeHtml(data.learner_level)} &nbsp; <strong>Goal:</strong> ${escapeHtml(data.goal)}</p>
    <div class="steps">${data.steps.map((s, i) => `<article class="step"><span class="step-number">${i+1}</span><div><h3>${escapeHtml(s.level)}: ${escapeHtml(s.topic)}</h3><p>${escapeHtml(s.why_it_matters)}</p><small>Estimated time: ${escapeHtml(s.estimated_time)}</small>${s.resources.length ? `<ul>${s.resources.map(r => `<li>${escapeHtml(r)}</li>`).join('')}</ul>` : ''}</div></article>`).join('')}</div>
    <h3>Study tips</h3><ul>${data.study_tips.map(t => `<li>${escapeHtml(t)}</li>`).join('')}</ul>`;
}

button.addEventListener('click', async () => {
  const text = input.value.trim();
  if (!text) { status.textContent = 'Please enter some text first.'; return; }
  button.disabled = true; status.textContent = 'EduGenie is thinking…'; result.classList.add('hidden');
  try {
    const response = await fetch(endpoints[task.value], {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text})});
    const responseText = await response.text();
    let data;
    try {
      data = responseText ? JSON.parse(responseText) : {};
    } catch {
      if (!response.ok) throw new Error(responseText || `Request failed (${response.status}).`);
      throw new Error('The server returned an invalid response. Check the server terminal for details.');
    }
    if (!response.ok) throw new Error(data.detail || 'Request failed.');
    if (task.value === 'quiz') result.innerHTML = renderQuiz(data);
    else if (task.value === 'learn') result.innerHTML = renderLearning(data);
    else result.innerHTML = renderText(data.answer || data.explanation || data.summary || JSON.stringify(data, null, 2));
    result.classList.remove('hidden'); status.textContent = 'Completed.';
  } catch (err) {
    status.textContent = err.message;
  } finally { button.disabled = false; }
});

result.addEventListener('click', event => {
  if (!event.target.classList.contains('option')) return;
  const btn = event.target; const correct = btn.dataset.answer === btn.dataset.value;
  const feedback = btn.closest('.quiz-question').querySelector('.feedback');
  feedback.hidden = false; feedback.textContent = correct ? '✓ Correct!' : `✗ Incorrect. Correct answer: ${btn.dataset.answer}`;
});
