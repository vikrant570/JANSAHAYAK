export default function PrivacyPolicyPage() {
    return (
        <main className="min-h-screen w-full md:min-w-screen py-12 px-4 sm:px-6 lg:px-8 bg-ui-background font-sans selection:bg-buttons selection:text-texts-primary">
            <div className="max-w-3xl md:max-w-screen mx-auto rounded-2rem bg-texts-primary text-texts-dark p-8 sm:p-12 md:p-16 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">

                {/* Header Section */}
                <header className="mb-10 pb-8 border-b border-ui-tertiary/30">
                    <h1 className="text-3xl sm:text-4xl font-bold tracking-tight mb-2">
                        Privacy Policy
                    </h1>
                    <p className="text-texts-secondary text-sm sm:text-base font-medium">
                        Last updated: 22 Aug, 2026
                    </p>
                </header>

                {/* Content Section */}
                <article className="space-y-10 leading-relaxed text-sm sm:text-base">

                    <section>
                        <p className="mb-4">
                            This Privacy Policy explains how <strong>JanSahayak</strong> collects, uses, stores, and protects your information when you use our platform to discover and understand government schemes and benefits you may be eligible for.
                        </p>
                        <p>
                            By using Jansahayak, you agree to the practices described in this policy.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl sm:text-2xl font-semibold mb-6">1. Information We Collect</h2>

                        <div className="space-y-6">
                            <div>
                                <h3 className="text-lg font-medium mb-2 text-buttons">1.1 Account Information</h3>
                                <ul className="list-disc pl-5 space-y-1 text-texts-secondary">
                                    <li><span className="text-texts-dark">Email address (for registration and verification)</span></li>
                                    <li><span className="text-texts-dark">Password (stored in encrypted/hashed form — we never store plain-text passwords)</span></li>
                                </ul>
                            </div>

                            <div>
                                <h3 className="text-lg font-medium mb-2 text-buttons">1.2 Chat and Conversation Data</h3>
                                <ul className="list-disc pl-5 space-y-1 text-texts-secondary">
                                    <li><span className="text-texts-dark">Messages you send to our AI assistant</span></li>
                                    <li><span className="text-texts-dark">AI-generated responses, including scheme recommendations and eligibility information</span></li>
                                    <li><span className="text-texts-dark">Session/chat history, stored so you can revisit past conversations</span></li>
                                </ul>
                            </div>

                            <div>
                                <h3 className="text-lg font-medium mb-2 text-buttons">1.3 Documents You Upload</h3>
                                <p className="mb-2">
                                    If you upload a document (for example, to check eligibility or extract details via OCR), the document is processed to extract relevant information.
                                </p>
                                <p className="mb-2">
                                    We do not permanently store uploaded documents. Documents are used only for the purpose you uploaded them for (e.g., OCR extraction) and are discarded after processing.
                                </p>
                                <p>
                                    If any extracted information from a document appears in your chat history (for example, as part of an AI response), that text may be retained as part of your chat history for your future reference, in the same way as any other message in the conversation.
                                </p>
                            </div>

                            <div>
                                <h3 className="text-lg font-medium mb-2 text-buttons">1.4 Sensitive Personal Information</h3>
                                <p>
                                    Depending on what you choose to share in conversation (for example, category such as SC/ST/OBC, income range, state of residence, or occupation), we may process this information solely to determine your eligibility for government schemes. This is information you voluntarily provide as part of your query — we do not independently collect or verify it from any external source.
                                </p>
                            </div>

                            <div>
                                <h3 className="text-lg font-medium mb-2 text-buttons">1.5 Technical Information</h3>
                                <p>
                                    Basic technical data such as IP address, browser type, and device information, collected automatically for security and app functionality (e.g., session management, fraud prevention).
                                </p>
                            </div>
                        </div>
                    </section>

                    <section>
                        <h2 className="text-xl sm:text-2xl font-semibold mb-4">2. How We Use Your Information</h2>
                        <p className="mb-4">We use the information collected only to:</p>
                        <ul className="list-disc pl-5 space-y-2 mb-4 text-texts-dark marker:text-buttons">
                            <li><span>Create and manage your account</span></li>
                            <li><span>Verify your email address</span></li>
                            <li><span>Process your queries and generate relevant scheme/benefit recommendations</span></li>
                            <li><span>Maintain your chat history so you can access past conversations</span></li>
                            <li><span>Improve the accuracy and relevance of our recommendations</span></li>
                            <li><span>Maintain the security and integrity of our platform</span></li>
                        </ul>
                        <p>
                            We do not use your personal or eligibility information for advertising, and we do not sell your data to any third party.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl sm:text-2xl font-semibold mb-4">3. Where Your Data Is Stored</h2>
                        <p>
                            All user data — account information, chat history, and any eligibility details you share — is stored on our own servers using MongoDB. We do not share this data with external AI providers, third-party analytics tools, or advertising networks beyond what is stated in this policy.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl sm:text-2xl font-semibold mb-4">4. Data Retention</h2>
                        <ul className="space-y-4">
                            <li>
                                <strong className="text-buttons font-semibold">Unverified accounts: </strong>
                                If you register but do not verify your email within 24 hours, your account and associated data are automatically and permanently deleted from our systems.
                            </li>
                            <li>
                                <strong className="text-buttons font-semibold">Verified accounts: </strong>
                                We retain your account and chat history for as long as your account remains active, or until you request deletion (see Section 6).
                            </li>
                            <li>
                                <strong className="text-buttons font-semibold">Uploaded documents: </strong>
                                Not retained after processing, as described in Section 1.3.
                            </li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl sm:text-2xl font-semibold mb-4">5. How We Protect Your Data</h2>
                        <ul className="list-disc pl-5 space-y-2 text-texts-secondary marker:text-buttons">
                            <li><span className="text-texts-dark">Passwords are stored using industry-standard hashing (never in plain text).</span></li>
                            <li><span className="text-texts-dark">Access to our database is restricted and secured.</span></li>
                            <li><span className="text-texts-dark">Chat sessions are tied to your authenticated account, so other users cannot access your conversations or data.</span></li>
                            <li><span className="text-texts-dark">We take reasonable technical and organizational measures to protect your data against unauthorized access, loss, or misuse.</span></li>
                        </ul>
                        <p className="mt-4 text-texts-secondary italic">
                            No system can guarantee absolute security, but we are committed to safeguarding your information to the best of our ability.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl sm:text-2xl font-semibold mb-4">6. Your Rights</h2>
                        <p className="mb-4">
                            As a user based in India, under the Digital Personal Data Protection Act, 2023 (DPDP Act), you have the right to:
                        </p>
                        <ul className="list-disc pl-5 space-y-2 mb-4 text-texts-secondary marker:text-buttons">
                            <li><span className="text-texts-dark">Access the personal data we hold about you</span></li>
                            <li><span className="text-texts-dark">Correct inaccurate or outdated information</span></li>
                            <li><span className="text-texts-dark">Withdraw consent for processing of your data at any time</span></li>
                            <li><span className="text-texts-dark">Request deletion of your account and associated data</span></li>
                            <li><span className="text-texts-dark">Grievance redressal — raise concerns about how your data is handled</span></li>
                        </ul>
                        <p>
                            To exercise any of these rights, contact us at <a href="mailto:support.jansahayakai@gmail.com" className="text-buttons hover:underline">support.jansahayakai@gmail.com</a>.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl sm:text-2xl font-semibold mb-4">7. Children's Privacy</h2>
                        <p>
                            JanSahayak is not intended for use by individuals under the age of 18 without appropriate guidance. We do not knowingly collect data from minors without consent from a parent or guardian.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl sm:text-2xl font-semibold mb-4">8. Changes to This Policy</h2>
                        <p>
                            We may update this Privacy Policy from time to time to reflect changes in our practices or for legal, operational, or regulatory reasons. We will notify users of significant changes via email or an in-app notice. Continued use of the platform after changes take effect constitutes acceptance of the updated policy.
                        </p>
                    </section>

                    <section className="bg-ui-background p-6 rounded-2xl mt-8">
                        <h2 className="text-xl sm:text-2xl font-semibold mb-4">9. Contact Us</h2>
                        <p className="mb-4">
                            If you have questions, concerns, or requests regarding this Privacy Policy or your personal data, please contact us at:
                        </p>
                        <div className="space-y-2">
                            <p><strong>Email:</strong> <a href="mailto:support.jansahayakai@gmail.com" className="text-buttons hover:underline">support.jansahayakai@gmail.com</a></p>
                            <p><strong>Address:</strong> Jansahayak </p>
                        </div>
                    </section>

                    <div className="mt-12 pt-6 border-t border-ui-tertiary/30 text-xs sm:text-sm text-texts-secondary text-center">
                        <p>
                            This policy is intended to comply with the Digital Personal Data Protection Act, 2023 (India). It is provided as a starting template and should be reviewed by a legal professional before formal publication, especially before handling sensitive eligibility data such as caste category or income at scale.
                        </p>
                    </div>

                </article>
            </div>
        </main>
    );
}
