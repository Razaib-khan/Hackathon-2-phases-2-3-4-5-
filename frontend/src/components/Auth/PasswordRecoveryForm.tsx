import React, { useState } from 'react';
import Link from 'next/link';

interface PasswordRecoveryFormData {
  email: string;
  favoriteTeacherAnswer: string;
}

const PasswordRecoveryForm: React.FC = () => {
  const [formData, setFormData] = useState<PasswordRecoveryFormData>({
    email: '',
    favoriteTeacherAnswer: '',
  });
  const [errors, setErrors] = useState<Partial<PasswordRecoveryFormData>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });

    // Clear error when user starts typing
    if (errors[name as keyof PasswordRecoveryFormData]) {
      setErrors({
        ...errors,
        [name]: undefined,
      });
    }
  };

  const validate = (): boolean => {
    const newErrors: Partial<PasswordRecoveryFormData> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email address is invalid';
    }

    if (!formData.favoriteTeacherAnswer) {
      newErrors.favoriteTeacherAnswer = 'Favorite teacher answer is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);

    try {
      // Simulate API call for password recovery
      // In a real application, you would call your backend API here
      console.log('Password recovery request:', formData);

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Reset form
      setFormData({ email: '', favoriteTeacherAnswer: '' });
      setSuccessMessage('Password recovery instructions sent to your email.');

      // Clear success message after 5 seconds
      setTimeout(() => {
        setSuccessMessage('');
      }, 5000);
    } catch (error) {
      console.error('Password recovery failed:', error);
      setErrors({
        email: 'Failed to send recovery instructions. Please try again.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Password Recovery</h2>

      <p className="text-gray-600 mb-6 text-center">
        Enter your email and answer your security question to recover your password
      </p>

      {successMessage && (
        <div className="mb-6 p-3 bg-green-100 border border-green-400 text-green-700 rounded mb-4">
          {successMessage}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email Address
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 ${
              errors.email ? 'border-red-500 focus:ring-red-200' : 'border-gray-300 focus:ring-blue-200'
            }`}
            placeholder="your@email.com"
          />
          {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email}</p>}
        </div>

        <div>
          <label htmlFor="favoriteTeacherAnswer" className="block text-sm font-medium text-gray-700 mb-1">
            What is the name of your favorite teacher?
          </label>
          <input
            type="text"
            id="favoriteTeacherAnswer"
            name="favoriteTeacherAnswer"
            value={formData.favoriteTeacherAnswer}
            onChange={handleChange}
            className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 ${
              errors.favoriteTeacherAnswer
                ? 'border-red-500 focus:ring-red-200'
                : 'border-gray-300 focus:ring-blue-200'
            }`}
            placeholder="Enter your answer"
          />
          {errors.favoriteTeacherAnswer && (
            <p className="mt-1 text-sm text-red-600">{errors.favoriteTeacherAnswer}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className={`w-full py-3 px-4 rounded-md text-white font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 ${
            isSubmitting
              ? 'bg-blue-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'
          }`}
        >
          {isSubmitting ? 'Sending...' : 'Recover Password'}
        </button>
      </form>

      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Remember your password?{' '}
          <Link href="/auth/signin" className="font-medium text-blue-600 hover:text-blue-500">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default PasswordRecoveryForm;