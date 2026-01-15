import React, { useState } from 'react';

interface PasswordChangeFormData {
  oldPassword: string;
  newPassword: string;
  confirmNewPassword: string;
}

interface PasswordChangeFormProps {
  onSubmit: (data: PasswordChangeFormData) => void;
  isLoading?: boolean;
}

const PasswordChangeForm: React.FC<PasswordChangeFormProps> = ({
  onSubmit,
  isLoading = false
}) => {
  const [formData, setFormData] = useState<PasswordChangeFormData>({
    oldPassword: '',
    newPassword: '',
    confirmNewPassword: ''
  });

  const [errors, setErrors] = useState<Partial<PasswordChangeFormData>>({});
  const [showPasswords, setShowPasswords] = useState({
    oldPassword: false,
    newPassword: false,
    confirmNewPassword: false
  });

  const validateForm = (): boolean => {
    const newErrors: Partial<PasswordChangeFormData> = {};

    if (!formData.oldPassword.trim()) {
      newErrors.oldPassword = 'Old password is required';
    }

    if (!formData.newPassword.trim()) {
      newErrors.newPassword = 'New password is required';
    } else if (formData.newPassword.length < 8) {
      newErrors.newPassword = 'Password must be at least 8 characters';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.newPassword)) {
      newErrors.newPassword = 'Password must contain uppercase, lowercase, and number';
    }

    if (!formData.confirmNewPassword.trim()) {
      newErrors.confirmNewPassword = 'Please confirm your new password';
    } else if (formData.newPassword !== formData.confirmNewPassword) {
      newErrors.confirmNewPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name as keyof PasswordChangeFormData]) {
      setErrors(prev => ({
        ...prev,
        [name]: undefined
      }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const togglePasswordVisibility = (field: keyof typeof showPasswords) => {
    setShowPasswords(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Change Password</h2>

      {/* Old Password Field */}
      <div className="mb-4">
        <label htmlFor="oldPassword" className="block text-sm font-medium text-gray-700 mb-1">
          Current Password
        </label>
        <div className="relative">
          <input
            id="oldPassword"
            name="oldPassword"
            type={showPasswords.oldPassword ? "text" : "password"}
            value={formData.oldPassword}
            onChange={handleChange}
            className={`w-full px-3 py-2 border ${
              errors.oldPassword ? "border-red-500" : "border-gray-300"
            } rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500`}
            placeholder="Enter your current password"
          />
          <button
            type="button"
            onClick={() => togglePasswordVisibility('oldPassword')}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
          >
            {showPasswords.oldPassword ? (
              <span className="text-gray-500">Hide</span>
            ) : (
              <span className="text-gray-500">Show</span>
            )}
          </button>
        </div>
        {errors.oldPassword && (
          <p className="mt-1 text-sm text-red-600">{errors.oldPassword}</p>
        )}
      </div>

      {/* New Password Field */}
      <div className="mb-4">
        <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-1">
          New Password
        </label>
        <div className="relative">
          <input
            id="newPassword"
            name="newPassword"
            type={showPasswords.newPassword ? "text" : "password"}
            value={formData.newPassword}
            onChange={handleChange}
            className={`w-full px-3 py-2 border ${
              errors.newPassword ? "border-red-500" : "border-gray-300"
            } rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500`}
            placeholder="Enter your new password"
          />
          <button
            type="button"
            onClick={() => togglePasswordVisibility('newPassword')}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
          >
            {showPasswords.newPassword ? (
              <span className="text-gray-500">Hide</span>
            ) : (
              <span className="text-gray-500">Show</span>
            )}
          </button>
        </div>
        {errors.newPassword && (
          <p className="mt-1 text-sm text-red-600">{errors.newPassword}</p>
        )}
      </div>

      {/* Confirm New Password Field */}
      <div className="mb-6">
        <label htmlFor="confirmNewPassword" className="block text-sm font-medium text-gray-700 mb-1">
          Confirm New Password
        </label>
        <div className="relative">
          <input
            id="confirmNewPassword"
            name="confirmNewPassword"
            type={showPasswords.confirmNewPassword ? "text" : "password"}
            value={formData.confirmNewPassword}
            onChange={handleChange}
            className={`w-full px-3 py-2 border ${
              errors.confirmNewPassword ? "border-red-500" : "border-gray-300"
            } rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500`}
            placeholder="Confirm your new password"
          />
          <button
            type="button"
            onClick={() => togglePasswordVisibility('confirmNewPassword')}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
          >
            {showPasswords.confirmNewPassword ? (
              <span className="text-gray-500">Hide</span>
            ) : (
              <span className="text-gray-500">Show</span>
            )}
          </button>
        </div>
        {errors.confirmNewPassword && (
          <p className="mt-1 text-sm text-red-600">{errors.confirmNewPassword}</p>
        )}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading}
        className={`w-full py-2 px-4 rounded-md text-white font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${
          isLoading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {isLoading ? "Changing Password..." : "Change Password"}
      </button>
    </form>
  );
};

export default PasswordChangeForm;