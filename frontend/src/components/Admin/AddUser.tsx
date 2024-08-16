import {
  Button,
  Checkbox,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Select,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons"
import { type UserCreate, UsersService } from "../../client"
import type { ApiError } from "../../client/core/ApiError"
import useCustomToast from "../../hooks/useCustomToast"
import { emailPattern, handleError } from "../../utils"

interface AddUserProps {
  isOpen: boolean
  onClose: () => void
}

interface UserCreateForm extends UserCreate {
  confirm_password: string
  avatar?: FileList
  roles: string[]
  is_superuser: boolean // Добавляем поле для чекбокса superuser
}

const AddUser = ({ isOpen, onClose }: AddUserProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    getValues,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<UserCreateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      email: "",
      name: "",
      surname: "",
      middle_name: "",
      birth_year: "",
      password: "",
      confirm_password: "",
      roles: [],
      is_superuser: false, // Инициализируем чекбокс как не выбранный
    },
  })

  const mutation = useMutation({
    mutationFn: (data: FormData) =>
      UsersService.createUser({ requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "User created successfully.", "success")
      reset()
      onClose()
    },
    onError: (err: ApiError) => {
      handleError(err, showToast)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] })
    },
  })

  const onSubmit: SubmitHandler<UserCreateForm> = (data) => {
    const formData = new FormData()
    formData.append("name", data.name)
    formData.append("surname", data.surname)
    formData.append("middle_name", data.middle_name)
    formData.append("birth_year", data.birth_year)
    formData.append("email", data.email)
    formData.append("password", data.password)
    formData.append("confirm_password", data.confirm_password)
    formData.append("roles", JSON.stringify(data.roles))
    formData.append("is_superuser", data.is_superuser.toString())
    if (data.avatar && data.avatar.length > 0) {
      formData.append("avatar", data.avatar[0])
    }

    mutation.mutate(formData)
  }

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <ModalOverlay />
        <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <ModalHeader>Add User</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isRequired isInvalid={!!errors.email}>
              <FormLabel htmlFor="email">Email</FormLabel>
              <Input
                id="email"
                {...register("email", {
                  required: "Email is required",
                  pattern: emailPattern,
                })}
                placeholder="Email"
                type="email"
              />
              {errors.email && (
                <FormErrorMessage>{errors.email.message}</FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4} isInvalid={!!errors.name}>
              <FormLabel htmlFor="name">Name</FormLabel>
              <Input
                id="name"
                {...register("name")}
                placeholder="Name"
                type="text"
              />
              {errors.name && (
                <FormErrorMessage>{errors.name.message}</FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4} isInvalid={!!errors.surname}>
              <FormLabel htmlFor="surname">Surname</FormLabel>
              <Input
                id="surname"
                {...register("surname")}
                placeholder="Surname"
                type="text"
              />
              {errors.surname && (
                <FormErrorMessage>{errors.surname.message}</FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4} isInvalid={!!errors.middle_name}>
              <FormLabel htmlFor="middle_name">Middle Name</FormLabel>
              <Input
                id="middle_name"
                {...register("middle_name")}
                placeholder="Middle Name"
                type="text"
              />
              {errors.middle_name && (
                <FormErrorMessage>{errors.middle_name.message}</FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4} isInvalid={!!errors.birth_year}>
              <FormLabel htmlFor="birth_year">Birth Year</FormLabel>
              <Input
                id="birth_year"
                {...register("birth_year")}
                placeholder="Birth Year"
                type="text"
              />
              {errors.birth_year && (
                <FormErrorMessage>{errors.birth_year.message}</FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4} isRequired isInvalid={!!errors.password}>
              <FormLabel htmlFor="password">Set Password</FormLabel>
              <Input
                id="password"
                {...register("password", {
                  required: "Password is required",
                  minLength: {
                    value: 8,
                    message: "Password must be at least 8 characters",
                  },
                })}
                placeholder="Password"
                type="password"
              />
              {errors.password && (
                <FormErrorMessage>{errors.password.message}</FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4} isRequired isInvalid={!!errors.confirm_password}>
              <FormLabel htmlFor="confirm_password">Confirm Password</FormLabel>
              <Input
                id="confirm_password"
                {...register("confirm_password", {
                  required: "Please confirm your password",
                  validate: (value) =>
                    value === getValues().password ||
                    "The passwords do not match",
                })}
                placeholder="Password"
                type="password"
              />
              {errors.confirm_password && (
                <FormErrorMessage>
                  {errors.confirm_password.message}
                </FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4}>
              <FormLabel htmlFor="avatar">Avatar</FormLabel>
              <Input
                id="avatar"
                type="file"
                accept="image/*"
                onChange={(e) => {
                  const files = e.target.files
                  if (files && files.length > 0) {
                    setValue("avatar", files)
                  }
                }}
              />
            </FormControl>

            <FormControl mt={4}>
              <FormLabel htmlFor="roles">Roles</FormLabel>
              <Select
                id="roles"
                {...register("roles", { required: "At least one role is required" })}
                placeholder="Select roles"
                multiple
              >
                <option value="ROLE_PORTAL_USER">User</option>
                <option value="ROLE_PORTAL_ADMIN">Admin</option>
                <option value="ROLE_PORTAL_SUPERADMIN">Superadmin</option>
              </Select>
              {errors.roles && (
                <FormErrorMessage>{errors.roles.message}</FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4}>
              <FormLabel htmlFor="is_superuser">Superuser</FormLabel>
              <Checkbox
                id="is_superuser"
                {...register("is_superuser")}
              >
                Superuser
              </Checkbox>
            </FormControl>
          </ModalBody>
          <ModalFooter gap={3}>
            <Button variant="primary" type="submit" isLoading={isSubmitting}>
              Save
            </Button>
            <Button onClick={onClose}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}

export default AddUser
