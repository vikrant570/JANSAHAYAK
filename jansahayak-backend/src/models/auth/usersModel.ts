import mongoose from "mongoose";

const nameValidator = {
  validator: function (v: string) {
    // Allows letters (upper/lower), spaces are optional, at least 3 characters
    return /^[A-Za-z]+(?: [A-Za-z]+)*$/.test(v) && v.replace(/ /g, '').length >= 3;
  },
  message: "Name can contain only alphabets !",
}

const userSchema = new mongoose.Schema({
  name: {
    first: {
      type: String,
      required: true,
      trim: true,
      validate: nameValidator,
    },
    last: {
      type: String,
      required: true,
      trim: true,
      validate: nameValidator,
    }
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true,
    match: [
      // Email regex
      /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/,
      "Please enter a valid email address !",
    ],
  },
  password: {
    type: String,
    required: true,
    minlength: 7,
    match: [
      // At least 1 uppercase, 1 lowercase, 1 number, 1 special char, min 7 chars
      // No spaces allowed in password
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{7,}$/,
      "Password must be at least 7 characters and include 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character.",
    ],
  },
  otherDetails: {
    age: {
      type: Number,
      min: 14,
      max: 100
    },
    state: {
      type: String,
      trim: true,
    },
    occupation: {
      type: String,
      trim: true,
      maxLength: 30,
      minLength: 4
    },
    income: {
      type: Number,
      max: 10000000,
      min: 0,
    },
    default: {}
  },
  isVerified: {
    type: Boolean,
    default: false
  }
})

userSchema.index(
  { createdAt: 1 },
  {
    expireAfterSeconds: 86400, // 1 day = 24 * 60 * 60
    partialFilterExpression: { isVerified: false }
  }
);

const Users = mongoose.model('users', userSchema);
export default Users;