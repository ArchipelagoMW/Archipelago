window.addEventListener('load', () => {

  // Handle changes to range inputs
  document.querySelectorAll('input[type=range]').forEach((range) => {
    const optionName = range.getAttribute('id');
    range.addEventListener('change', () => {
      document.getElementById(`${optionName}-value`).innerText = range.value;

      // Handle updating named range selects to "custom" if appropriate
      const select = document.querySelector(`select[data-option-name=${optionName}]`);
      if (select) {
        let updated = false;
        select?.childNodes.forEach((option) => {
          if (option.value === range.value) {
            select.value = range.value;
            updated = true;
          }
        });
        if (!updated) {
          select.value = 'custom';
        }
      }
    });
  });

  // Handle changes to named range selects
  document.querySelectorAll('.named-range-container select').forEach((select) => {
    const optionName = select.getAttribute('data-option-name');
    select.addEventListener('change', (evt) => {
      document.getElementById(optionName).value = evt.target.value;
      document.getElementById(`${optionName}-value`).innerText = evt.target.value;
    });
  });

  // Handle changes to randomize checkboxes
  document.querySelectorAll('.randomize-checkbox').forEach((checkbox) => {
    const optionName = checkbox.getAttribute('data-option-name');
    checkbox.addEventListener('change', () => {
      const optionInput = document.getElementById(optionName);
      const namedRangeSelect = document.querySelector(`select[data-option-name=${optionName}]`);
      if (checkbox.checked) {
        optionInput.setAttribute('disabled', '1');
        namedRangeSelect?.setAttribute('disabled', '1');
      } else {
        optionInput.removeAttribute('disabled');
        namedRangeSelect?.removeAttribute('disabled');
      }
    });
  });

  // Handle changes to TextChoice input[type=text]
  document.querySelectorAll('.text-choice-container input[type=text]').forEach((input) => {
    const optionName = input.getAttribute('data-option-name');
    input.addEventListener('input', () => {
      const select = document.getElementById(optionName);
      const optionValues = [];
      select.childNodes.forEach((option) => optionValues.push(option.value));
      select.value = (optionValues.includes(input.value)) ? input.value : 'custom';
    });
  });

  // Handle changes to TextChoice select
  document.querySelectorAll('.text-choice-container select').forEach((select) => {
    const optionName = select.getAttribute('id');
    select.addEventListener('change', () => {
      document.getElementById(`${optionName}-custom`).value = '';
    });
  });
});
