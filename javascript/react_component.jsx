/**
 * React Component Template
 * 
 * Template for creating a functional React component with hooks.
 */

import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const ComponentName = ({ prop1, prop2, onEvent }) => {
  // State management
  const [state, setState] = useState(initialValue);

  // Side effects
  useEffect(() => {
    // Effect logic here
    
    // Cleanup function (optional)
    return () => {
      // Cleanup logic
    };
  }, [/* dependencies */]);

  // Event handlers
  const handleClick = () => {
    // Handle click logic
    if (onEvent) {
      onEvent(data);
    }
  };

  // Render
  return (
    <div className="component-name">
      <h2>{prop1}</h2>
      <button onClick={handleClick}>
        Click Me
      </button>
      {prop2 && <p>{prop2}</p>}
    </div>
  );
};

// PropTypes for type checking
ComponentName.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.string,
  onEvent: PropTypes.func,
};

// Default props
ComponentName.defaultProps = {
  prop2: null,
  onEvent: null,
};

export default ComponentName;
