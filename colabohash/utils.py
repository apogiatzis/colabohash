def expand_shadow_element(driver, element):
  return driver.execute_script('return arguments[0].shadowRoot', element)
